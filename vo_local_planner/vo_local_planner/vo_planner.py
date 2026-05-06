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

        # 1. QoS Profile 정의 (구독자 생성 전에 반드시 필요)
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # 2. 클래스 변수 초기화 (Numpy로 통일)
        self.drone_pos = np.array([0.0, 0.0, 0.0])  # x, y, z
        self.drone_vel = np.array([0.0, 0.0, 0.0])  # vx, vy, vz
        self.obs_pos = np.array([0.0, 0.0])
        self.obs_vel = np.array([0.0, 0.0])
        
        self.robot_radius = 0.5
        self.obs_radius = 3.0
        self.desired_velocity = np.array([1.0, 0.0])
        self.current_obstacles = []

        # 3. 구독자 및 발행자 설정
        self.obstacle_sub = self.create_subscription(
            ObstacleArray,
            '/obstacle_states',
            self.obstacle_callback, # 하단에 정의된 메서드 연결
            10
        )

        self.odom_sub = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,     # 하단에 정의된 메서드 연결
            qos_profile
        )

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # 4. 타이머 설정
        self.timer = self.create_timer(0.1, self.plan)

    # --- 콜백 함수들을 __init__ 밖으로 이동 (들여쓰기 주의) ---

    def odom_callback(self, msg):
        # 위치 업데이트 (NED)
        self.drone_pos[0] = msg.position[0]
        self.drone_pos[1] = msg.position[1]
        self.drone_pos[2] = msg.position[2]
        # 속도 업데이트 (NED)
        self.drone_vel[0] = msg.velocity[0]
        self.drone_vel[1] = msg.velocity[1]
        self.drone_vel[2] = msg.velocity[2]
        
        self.get_logger().info(f"Pos: {self.drone_pos}, Vel: {self.drone_vel}")

    def obstacle_callback(self, msg):
        self.current_obstacles = msg.obstacles 
        if len(msg.obstacles) > 0:
            # 현재 드론 위치(x, y)와 가장 가까운 장애물 찾기
            closest_obs = min(msg.obstacles, key=lambda obs: np.linalg.norm(
                self.drone_pos[:2] - np.array([obs.position.x, obs.position.y])))
            
            self.obs_pos = np.array([closest_obs.position.x, closest_obs.position.y])
            self.obs_vel = np.array([closest_obs.velocity.x, closest_obs.velocity.y])
            self.obs_radius = closest_obs.radius

    # --- 나머지 기하학적 연산 및 플래닝 로직 ---
    def in_vo(self, v):
        # self.drone_pos[:2]를 사용하여 x, y만 추출해서 연산
        rel_pos = self.obs_pos - self.drone_pos[:2] 
        rel_vel = v - self.obs_vel
        # ... (이후 로직 동일)
        dist = np.linalg.norm(rel_pos)
        combined_radius = self.robot_radius + self.obs_radius
        if dist < combined_radius: return True
        
        theta = np.arcsin(np.clip(combined_radius / dist, -1.0, 1.0))
        direction = rel_pos / dist
        vel_dir = rel_vel / (np.linalg.norm(rel_vel) + 1e-5)
        angle = np.arccos(np.clip(np.dot(direction, vel_dir), -1.0, 1.0))
        return angle < theta

    def sample_velocities(self):
        samples = []
        for vx in np.linspace(-2, 2, 15):
            for vy in np.linspace(-2, 2, 15):
                samples.append(np.array([vx, vy]))
        return samples

    def plan(self):
        candidates = self.sample_velocities()
        safe_velocities = [v for v in candidates if not self.in_vo(v)]

        if not safe_velocities:
            v_safe = np.array([0.0, 0.0])
        else:
            costs = [np.linalg.norm(v - self.desired_velocity) for v in safe_velocities]
            v_safe = safe_velocities[np.argmin(costs)]

        cmd = Twist()
        cmd.linear.x = float(v_safe[0])
        cmd.linear.y = float(v_safe[1])
        self.cmd_pub.publish(cmd)

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