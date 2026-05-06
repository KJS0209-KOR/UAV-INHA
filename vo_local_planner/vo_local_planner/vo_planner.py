import rclpy
from rclpy.node import Node
import numpy as np
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# 메시지 타입들
from px4_msgs.msg import VehicleOdometry
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry #드론의 위치, 속도를 받는 메시지 관련 토픽
#UBUNTU 들어가서 어떤 메시지 타입이 있는지 다 봐야해!!!

from px4_msgs.msg import VehicleOdometry
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# 장애물 배열 전체를 받기 위한 타입(obstacle_state_publisher와의 연결)
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

        self.received_drone_odom = False
        self.received_obstacles = False

        # obstacle pose
        self.obs_pos = np.array([0.0, 0.0])
        self.obs_vel = np.array([0.0, 0.0])
        self.current_obstacles = []

        # robot / obstacle radius
        self.robot_radius = 0.5 #0.4~0.5 사이에서 조절을 해보자.
        self.obs_radius = 3 #장애물의 크기도 받아서 바꾸자.

        # 목표 속도
        self.desired_velocity = np.array([1.0, 0.0])
        self.current_obstacles = []


        def obstacle_array_callback(self, msg):
            # 수신된 장애물의 개수를 터미널에 출력
            self.get_logger().info(f"수신된 장애물 개수: {len(msg.obstacles)}")
    
            for obs in msg.obstacles:
            # 특정 장애물의 좌표와 속도를 확인
                self.get_logger().debug(f"ID: {obs.id} | Pos: ({obs.position.x:.2f}, {obs.position.y:.2f}) | Vel: {obs.velocity.x:.2f}")
    
            # 데이터를 클래스 변수에 저장
            self.current_obstacles = msg.obstacles

        px4_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # subscriber, drone pose를 받는다. from gazebo topic
        self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.drone_callback,
            px4_qos
        )

        # vo_planner 노드 내부 예시
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

    def drone_callback(self, msg):  #drone의 위치를 받는 함수
        self.drone_pos = np.array([
            msg.position[0],
            msg.position[1]
        ])

        self.drone_vel = np.array([
            msg.velocity[0],
            msg.velocity[1]
        ])

        self.received_drone_odom = True

        self.get_logger().info(
            f"Drone odom received | pos=({self.drone_pos[0]:.2f}, {self.drone_pos[1]:.2f}) | vel=({self.drone_vel[0]:.2f}, {self.drone_vel[1]:.2f})",
            throttle_duration_sec=1.0
        )
 

    def obstacle_callback(self, msg):
        self.current_obstacles = msg.obstacles 
        self.received_obstacles = True

        obstacle_infos = []

        for obs in msg.obstacles:
            obstacle_infos.append(
                f"{obs.id}: pos=({obs.position.x:.2f}, {obs.position.y:.2f}), "
                f"vel=({obs.velocity.x:.2f}, {obs.velocity.y:.2f}), "
                f"radius={obs.radius:.2f}, static={obs.is_static}"
            )

        self.get_logger().info(
            f"ObstacleArray received | count={len(msg.obstacles)} | " + " | ".join(obstacle_infos),
            throttle_duration_sec=1.0
        )
    
    # 2. (선택 사항) 만약 기존 코드(단일 장애물 처리)를 유지하고 싶다면
    # 가장 가까운 장애물 하나만 골라서 업데이트 할 수도 있습니다.
        if len(msg.obstacles) > 0:
            # 현재 드론 위치(x, y)와 가장 가까운 장애물 찾기
            closest_obs = min(msg.obstacles, key=lambda obs: np.linalg.norm(
            self.drone_pos - np.array([obs.position.x, obs.position.y])))
        
        # 이제 이 하나의 장애물에 대해 위치와 속도를 '동시에' 업데이트
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
        if not self.received_drone_odom:
            self.get_logger().warn(
                "Waiting for /fmu/out/vehicle_odometry...",
                throttle_duration_sec=2.0
            )
            return

        if not self.received_obstacles:
            self.get_logger().warn(
                "Waiting for /obstacle_states...",
                throttle_duration_sec=2.0
            )
            return

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