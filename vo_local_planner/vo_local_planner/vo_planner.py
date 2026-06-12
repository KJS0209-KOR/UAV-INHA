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

        # [Mission target] Gazebo (34, 0, 5) -> PX4 local (0, 34, -5)
        self.target_xy = np.array([0.0, 34.0])

        self.wp_threshold = 1.0
        self.slowdown_radius = 2.0
        self.max_speed = 3.0

        # [Robot / obstacle parameters]
        self.robot_radius = 0.5
        self.default_obs_radius = 3.0
        
        # --- [추가 설정: 시간 지평] ---
        self.time_horizon = 4.0 

        self.received_drone_odom = False
        self.received_obstacles = False
        self.drone_pos = np.array([0.0, 0.0])
        self.drone_vel = np.array([0.0, 0.0])
        self.drone_z = 0.0
        self.current_obstacles = []
        self.goal_reached = False

        px4_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.create_subscription(VehicleOdometry, '/fmu/out/vehicle_odometry', self.drone_callback, px4_qos)
        self.create_subscription(ObstacleArray, '/obstacle_states', self.obstacle_callback, 10)
        
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.goal_reached_pub = self.create_publisher(Bool, '/goal_reached', 10)

        self.timer = self.create_timer(0.1, self.plan)
        self.get_logger().info(f"VO Planner (Time Horizon 적용) 시작. Target: {self.target_xy}")

    def drone_callback(self, msg):
        self.drone_pos = np.array([msg.position[0], msg.position[1]])
        self.drone_vel = np.array([msg.velocity[0], msg.velocity[1]])
        self.drone_z = msg.position[2]
        self.received_drone_odom = True

    def obstacle_callback(self, msg):
        self.current_obstacles = msg.obstacles
        self.received_obstacles = True

    def sample_velocities(self):
        samples = []
        # 속도 후보군 생성 (정밀도를 높이려면 격자 수를 늘리거나 polar sampling 고려)
        for vx in np.linspace(-self.max_speed, self.max_speed, 15):
            for vy in np.linspace(-self.max_speed, self.max_speed, 15):
                samples.append(np.array([vx, vy]))
        return samples

    def is_in_vo(self, candidate_vel, obs):
        obs_pos = np.array([obs.position.x, obs.position.y])
        obs_vel = np.array([obs.velocity.x, obs.velocity.y])
        obs_radius = obs.radius if obs.radius > 0.0 else self.default_obs_radius

        rel_pos = obs_pos - self.drone_pos
        rel_vel = candidate_vel - obs_vel 

        dist = np.linalg.norm(rel_pos)
        combined_radius = self.robot_radius + obs_radius

        if dist < combined_radius:
            return True

        theta = np.arcsin(np.clip(combined_radius / dist, -1.0, 1.0))
        direction_to_obs = rel_pos / dist
        rel_vel_norm = np.linalg.norm(rel_vel)

        if rel_vel_norm < 1e-5:
            return False

        rel_vel_dir = rel_vel / rel_vel_norm
        angle = np.arccos(np.clip(np.dot(direction_to_obs, rel_vel_dir), -1.0, 1.0))

        if angle < theta:
            dist_to_surface = dist - combined_radius
            time_to_collision = dist_to_surface / rel_vel_norm
            
            if time_to_collision < self.time_horizon:
                return True

        return False

    def compute_desired_velocity(self):
        rel_target_pos = self.target_xy - self.drone_pos
        dist_to_target = np.linalg.norm(rel_target_pos)

        if dist_to_target < 1e-5:
            return np.array([0.0, 0.0]), dist_to_target, rel_target_pos

        if dist_to_target < self.slowdown_radius:
            current_speed = max(self.max_speed * (dist_to_target / self.slowdown_radius), 0.1)
        else:
            current_speed = self.max_speed

        desired_velocity = (rel_target_pos / dist_to_target) * current_speed
        return desired_velocity, dist_to_target, rel_target_pos

    def plan(self):
        if not self.received_drone_odom:
            return

        if self.goal_reached:
            self.publish_velocity(0.0, 0.0)
            self.publish_goal_reached(True)
            return

        desired_velocity, dist_to_target, rel_target_pos = self.compute_desired_velocity()

        if dist_to_target < self.wp_threshold:
            self.get_logger().info("★★★ 목표 도달! ★★★")
            self.goal_reached = True
            self.publish_velocity(0.0, 0.0)
            self.publish_goal_reached(True)
            return

        if not self.received_obstacles or len(self.current_obstacles) == 0:
            self.publish_velocity(desired_velocity[0], desired_velocity[1])
            return

        candidates = self.sample_velocities()
        safe_velocities = []

        for v_cand in candidates:
            is_safe = True
            for obs in self.current_obstacles:
                if self.is_in_vo(v_cand, obs):
                    is_safe = False
                    break
            if is_safe:
                safe_velocities.append(v_cand)

        if not safe_velocities:
            final_velocity = np.array([0.0, 0.0])
            self.get_logger().warn("위험: 안전 속도 없음 (정지)")
        else:
            costs = [np.linalg.norm(v - desired_velocity) for v in safe_velocities]
            final_velocity = safe_velocities[int(np.argmin(costs))]

        self.publish_velocity(final_velocity[0], final_velocity[1])
        self.publish_goal_reached(False)

    def publish_velocity(self, vx, vy):
        cmd = Twist()
        cmd.linear.x = float(vx)
        cmd.linear.y = float(vy)
        # 필요 시 고도 유지를 위해 cmd.linear.z 제어 로직 추가 가능
        self.cmd_pub.publish(cmd)

    def publish_goal_reached(self, reached):
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