import rclpy
from rclpy.node import Node
import numpy as np
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# 메시지 타입들
from px4_msgs.msg import VehicleOdometry
from geometry_msgs.msg import Twist
from uav_interfaces.msg import ObstacleArray, Obstacle

class VOPlanner(Node):
    def __init__(self):
        super().__init__('vo_planner')

        # waypoint가 1개만 존재한다.
        self.waypoints = [
            np.array([10.0, 5.0])  # 목표 지점 딱 하나만 설정
        ]
        self.current_wp_idx = 0
        self.wp_threshold = 0.5  
        self.max_speed = 1.0     

        # 변수 초기화 (기존 로직 유지)
        self.received_drone_odom = False
        self.received_obstacles = False
        self.drone_pos = np.array([0.0, 0.0])
        self.drone_vel = np.array([0.0, 0.0])
        self.obs_pos = np.array([0.0, 0.0])
        self.obs_vel = np.array([0.0, 0.0])
        self.obs_radius = 3.0
        self.robot_radius = 0.5
        self.current_obstacles = []

        # QoS 설정
        px4_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # 구독 및 발행
        self.create_subscription(VehicleOdometry, '/fmu/out/vehicle_odometry', self.drone_callback, px4_qos) #이 토픽을 통해서 드론의 위치, 속도를 인지한다.
        self.obstacle_sub = self.create_subscription(ObstacleArray, '/obstacle_states', self.obstacle_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10) #속도를 직접 보내는 부분!!!

        # 타이머
        self.timer = self.create_timer(0.1, self.plan)

    def drone_callback(self, msg):
        self.drone_pos = np.array([msg.position[0], msg.position[1]]) #일단 현재는 2차원에서만 생각한다!!!
        self.drone_vel = np.array([msg.velocity[0], msg.velocity[1]])
        self.received_drone_odom = True

    def obstacle_callback(self, msg):
        self.current_obstacles = msg.obstacles
        self.received_obstacles = True
        if len(msg.obstacles) > 0:
            closest_obs = min(msg.obstacles, key=lambda obs: np.linalg.norm(
                self.drone_pos - np.array([obs.position.x, obs.position.y])))
            self.obs_pos = np.array([closest_obs.position.x, closest_obs.position.y])
            self.obs_vel = np.array([closest_obs.velocity.x, closest_obs.velocity.y])
            self.obs_radius = closest_obs.radius

    def sample_velocities(self):
        samples = []
        for vx in np.linspace(-2, 2, 15):
            for vy in np.linspace(-2, 2, 15):
                samples.append(np.array([vx, vy]))
        return samples        

    def in_vo(self, v):
        rel_pos = self.obs_pos - self.drone_pos
        rel_vel = v - self.obs_vel
        dist = np.linalg.norm(rel_pos)
        combined_radius = self.robot_radius + self.obs_radius
        if dist < combined_radius: return True
        
        theta = np.arcsin(np.clip(combined_radius / dist, -1.0, 1.0))
        direction = rel_pos / dist
        vel_dir = rel_vel / (np.linalg.norm(rel_vel) + 1e-5)
        angle = np.arccos(np.clip(np.dot(direction, vel_dir), -1.0, 1.0))
        return angle < theta

    

    def plan(self):
        if not self.received_drone_odom or not self.received_obstacles:
            return

        target_pos = self.waypoints[self.current_wp_idx]  #target_pos에는 당연히 목표점 좌표가 들어가야 한다.
        rel_target_pos = target_pos - self.drone_pos
        dist_to_target = np.linalg.norm(rel_target_pos)

        if dist_to_target < self.wp_threshold:
            self.get_logger().info("★★★ 목표 도달! ★★★")
            self.publish_velocity(0.0, 0.0)
            return

        slowdown_radius = 2.0 

        if dist_to_target < slowdown_radius:
            current_speed = max(self.max_speed * (dist_to_target / slowdown_radius), 0.1)
        else:
            current_speed = self.max_speed

        self.desired_velocity = (rel_target_pos / (dist_to_target + 1e-5)) * current_speed #목표점을 향해 정렬된 속도 벡터
        
        self.get_logger().info(
            f"-> [Step 1] Dist: {dist_to_target:.2f} | Rel_Pos: ({rel_target_pos[0]:.2f}, {rel_target_pos[1]:.2f}) | Desired_V: ({self.desired_velocity[0]:.2f}, {self.desired_velocity[1]:.2f})"
        )

        candidates = self.sample_velocities()  
        safe_velocities = []

        for v in candidates:
            is_safe = True
            for obs in self.current_obstacles:
                self.obs_pos = np.array([obs.position.x, obs.position.y])
                self.obs_vel = np.array([obs.velocity.x, obs.velocity.y])
                self.obs_radius = obs.radius
                if self.in_vo(v):
                    is_safe = False
                    break
            if is_safe:
                safe_velocities.append(v)

        # [로그 2] 안전 속도 샘플링 결과 확인
        # 만약 Safe Velocity 개수가 너무 적으면 VO 판정이 너무 엄격한(Radius가 너무 큰) 것입니다.
        self.get_logger().info(f"-> [Step 2] Safe Samples: {len(safe_velocities)} / {len(candidates)}")

        if not safe_velocities:
            v_safe = np.array([0.0, 0.0])
            self.get_logger().warn("!!! 위험: 안전한 속도가 없습니다 !!!")
        else:
            costs = [np.linalg.norm(v - self.desired_velocity) for v in safe_velocities]
            v_safe = safe_velocities[np.argmin(costs)]

        # [로그 3] 최종 결정된 속도 발행
        self.get_logger().info(
            f"-> [Step 3] FINAL CMD: ({v_safe[0]:.2f}, {v_safe[1]:.2f})\n" + "-"*50
        )
        self.publish_velocity(v_safe[0], v_safe[1])



    def publish_velocity(self, vx, vy):
        cmd = Twist()
        cmd.linear.x = float(vx)
        cmd.linear.y = float(vy)
        cmd.linear.z = 0.0
        self.cmd_pub.publish(cmd) #여기에서 사용하는 속도가 진짜로 드론이 움직이는 속도가 될거야. 여기를 분석해보자!!


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