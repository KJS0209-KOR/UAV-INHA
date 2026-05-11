#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import numpy as np

from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

from px4_msgs.msg import VehicleOdometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

from uav_interfaces.msg import ObstacleArray


class VOPlanner(Node):
    def __init__(self):
        super().__init__('vo_planner')

        # ============================================================
        # Mission target
        # ============================================================
        # Gazebo world 기준 목표점:
        #   (x, y, z) = (34, 0, 5)
        #
        # 현재 planner는 PX4 local x-y 기준으로 계산함.
        # 기존 Gazebo -> PX4 변환을 고려하면:
        #   PX4 x = Gazebo y
        #   PX4 y = Gazebo x
        #   PX4 z = -Gazebo z
        #
        # 따라서 Gazebo (34, 0, 5)
        #   -> PX4 local (0, 34, -5)
        #
        # planner는 2D만 사용하므로 waypoint는 [0, 34]
        self.target_xy = np.array([0.0, 34.0])

        self.wp_threshold = 1.0       # 목표 도달 판정 반경 [m]
        self.slowdown_radius = 2.0    # 목표 근처 감속 시작 반경 [m]
        self.max_speed = 3.0          # 최대 평면 속도 [m/s]

        # ============================================================
        # Robot / obstacle parameters
        # ============================================================
        self.robot_radius = 0.5
        self.default_obs_radius = 3.0

        # ============================================================
        # State variables
        # ============================================================
        self.received_drone_odom = False
        self.received_obstacles = False

        self.drone_pos = np.array([0.0, 0.0])
        self.drone_vel = np.array([0.0, 0.0])
        self.drone_z = 0.0

        self.current_obstacles = []

        self.goal_reached = False

        # ============================================================
        # QoS
        # ============================================================
        px4_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # ============================================================
        # Subscribers
        # ============================================================
        self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.drone_callback,
            px4_qos
        )

        self.create_subscription(
            ObstacleArray,
            '/obstacle_states',
            self.obstacle_callback,
            10
        )

        # ============================================================
        # Publishers
        # ============================================================
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.goal_reached_pub = self.create_publisher(
            Bool,
            '/goal_reached',
            10
        )

        # ============================================================
        # Timer
        # ============================================================
        self.timer = self.create_timer(0.1, self.plan)

        self.get_logger().info(
            f"VO Planner started. "
            f"Target XY(PX4 local) = ({self.target_xy[0]:.2f}, {self.target_xy[1]:.2f})"
        )

    def drone_callback(self, msg):
        """
        PX4 vehicle odometry 기준 드론 위치/속도 수신.

        현재 planner는 2D VO planner이므로 x, y만 사용한다.
        z는 로그 확인용으로만 저장한다.
        """
        self.drone_pos = np.array([
            msg.position[0],
            msg.position[1]
        ])

        self.drone_vel = np.array([
            msg.velocity[0],
            msg.velocity[1]
        ])

        self.drone_z = msg.position[2]

        self.received_drone_odom = True

    def obstacle_callback(self, msg):
        """
        obstacle_state_publisher에서 들어온 장애물 상태 저장.

        obstacle_states도 PX4 local 기준으로 변환되어 있다고 가정한다.
        """
        self.current_obstacles = msg.obstacles
        self.received_obstacles = True

    def sample_velocities(self):
        """
        후보 속도 샘플링.

        출력 속도는 PX4 local x-y 기준이다.
        """
        samples = []

        for vx in np.linspace(-self.max_speed, self.max_speed, 15):
            for vy in np.linspace(-self.max_speed, self.max_speed, 15):
                samples.append(np.array([vx, vy]))

        return samples

    def is_in_vo(self, candidate_vel, obs):
        """
        특정 장애물 obs에 대해 candidate_vel이 VO 영역 안에 있는지 판단.
        """
        obs_pos = np.array([
            obs.position.x,
            obs.position.y
        ])

        obs_vel = np.array([
            obs.velocity.x,
            obs.velocity.y
        ])

        obs_radius = obs.radius
        if obs_radius <= 0.0:
            obs_radius = self.default_obs_radius

        rel_pos = obs_pos - self.drone_pos
        rel_vel = candidate_vel - obs_vel

        dist = np.linalg.norm(rel_pos)
        combined_radius = self.robot_radius + obs_radius

        if dist < combined_radius:
            return True

        if dist < 1e-5:
            return True

        theta = np.arcsin(
            np.clip(combined_radius / dist, -1.0, 1.0)
        )

        direction_to_obs = rel_pos / dist

        rel_vel_norm = np.linalg.norm(rel_vel)

        if rel_vel_norm < 1e-5:
            return False

        rel_vel_dir = rel_vel / rel_vel_norm

        angle = np.arccos(
            np.clip(np.dot(direction_to_obs, rel_vel_dir), -1.0, 1.0)
        )

        return angle < theta

    def compute_desired_velocity(self):
        """
        목표점을 향하는 desired velocity 계산.
        """
        rel_target_pos = self.target_xy - self.drone_pos
        dist_to_target = np.linalg.norm(rel_target_pos)

        if dist_to_target < 1e-5:
            return np.array([0.0, 0.0]), dist_to_target, rel_target_pos

        if dist_to_target < self.slowdown_radius:
            current_speed = max(
                self.max_speed * (dist_to_target / self.slowdown_radius),
                0.1
            )
        else:
            current_speed = self.max_speed

        desired_velocity = (rel_target_pos / dist_to_target) * current_speed

        return desired_velocity, dist_to_target, rel_target_pos

    def plan(self):
        """
        VO planning main loop.
        """
        if not self.received_drone_odom:
            self.get_logger().warn("Waiting for drone odometry...")
            return

        if self.goal_reached:
            self.publish_velocity(0.0, 0.0)
            self.publish_goal_reached(True)
            return

        desired_velocity, dist_to_target, rel_target_pos = self.compute_desired_velocity()

        self.get_logger().info(
            f"-> [Target] "
            f"Drone(PX4)=({self.drone_pos[0]:.2f}, {self.drone_pos[1]:.2f}, z={self.drone_z:.2f}), "
            f"Target(PX4)=({self.target_xy[0]:.2f}, {self.target_xy[1]:.2f}), "
            f"Dist={dist_to_target:.2f}, "
            f"Rel=({rel_target_pos[0]:.2f}, {rel_target_pos[1]:.2f}), "
            f"Desired=({desired_velocity[0]:.2f}, {desired_velocity[1]:.2f})"
        )

        # ============================================================
        # Goal reached
        # ============================================================
        if dist_to_target < self.wp_threshold:
            self.get_logger().info("★★★ 목표 도달! Landing trigger publish. ★★★")

            self.goal_reached = True

            self.publish_velocity(0.0, 0.0)
            self.publish_goal_reached(True)

            return

        # ============================================================
        # 장애물 정보가 없으면 desired velocity 그대로 사용
        # ============================================================
        if not self.received_obstacles or len(self.current_obstacles) == 0:
            self.get_logger().warn(
                "No obstacle data received. Publishing desired velocity directly."
            )

            self.publish_velocity(
                desired_velocity[0],
                desired_velocity[1]
            )

            self.publish_goal_reached(False)
            return

        # ============================================================
        # VO candidate evaluation
        # ============================================================
        candidates = self.sample_velocities()
        safe_velocities = []

        for candidate_vel in candidates:
            is_safe = True

            for obs in self.current_obstacles:
                if self.is_in_vo(candidate_vel, obs):
                    is_safe = False
                    break

            if is_safe:
                safe_velocities.append(candidate_vel)

        self.get_logger().info(
            f"-> [VO] Safe Samples: {len(safe_velocities)} / {len(candidates)}"
        )

        if not safe_velocities:
            final_velocity = np.array([0.0, 0.0])
            self.get_logger().warn("!!! 위험: 안전한 속도가 없습니다. 정지 명령 발행 !!!")
        else:
            costs = [
                np.linalg.norm(v - desired_velocity)
                for v in safe_velocities
            ]

            final_velocity = safe_velocities[int(np.argmin(costs))]

        self.get_logger().info(
            f"-> [CMD] FINAL CMD: "
            f"vx={final_velocity[0]:.2f}, vy={final_velocity[1]:.2f}\n"
            + "-" * 60
        )

        self.publish_velocity(
            final_velocity[0],
            final_velocity[1]
        )

        self.publish_goal_reached(False)

    def publish_velocity(self, vx, vy):
        """
        controller_node로 x-y 평면 속도 명령 전달.

        현재 vx, vy는 이미 PX4 local 기준이라고 본다.
        따라서 controller_node에서 y축 부호를 다시 뒤집으면 안 된다.
        """
        cmd = Twist()

        cmd.linear.x = float(vx)
        cmd.linear.y = float(vy)
        cmd.linear.z = 0.0

        cmd.angular.x = 0.0
        cmd.angular.y = 0.0
        cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)

    def publish_goal_reached(self, reached):
        """
        목표 도달 여부 publish.

        controller_node는 /goal_reached가 true가 되면 착륙 명령을 보내면 된다.
        """
        msg = Bool()
        msg.data = bool(reached)

        self.goal_reached_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = VOPlanner()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()  
