import rclpy
from rclpy.node import Node

#ROS 토픽은 그냥 데이터가 아니라 정해진 메시지 타입을 사용합니다.
#Python 코드에서 이 타입을 사용하려면 import를 해야 합니다.
#geometry_msgs에 어떤 메시지 타입들이 존재하는지 알아야 한다.
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry #드론의 위치, 속도를 받는 메시지 관련 토픽
#UBUNTU 들어가서 어떤 메시지 타입이 있는지 다 봐야해!!!

from px4_msgs.msg import VehicleOdometry
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# 장애물 배열 전체를 받기 위한 타입(obstacle_state_publisher와의 연결)
from uav_interfaces.msg import ObstacleArray, Obstacle






import numpy as np


class VOPlanner(Node):

    def __init__(self):
        super().__init__('vo_planner')

        # drone pose, 메시지 받기 전에 0으로 초기화하는 작업
        self.drone_pos = np.array([0.0, 0.0])
        self.drone_vel = np.array([0.0, 0.0])

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
            '/obstacle_states',     # 방송 채널 이름 일치
            self.obstacle_callback, # 데이터를 받으면 실행할 함수
            10
        )


        self.pose = None
        self.vel = None

       
        # publisher(로봇에게 속도 명령을 내린다.)
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # planner timer
        self.timer = self.create_timer(
            0.1,
            self.plan
        )


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
   
    # 1. 장애물 정보를 리스트로 저장 (전체 파악)
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
        # 드론과 가장 가까운 거리에 있는 장애물을 찾는 로직
            closest_obs = min(msg.obstacles, key=lambda obs: np.linalg.norm(
            self.drone_pos - np.array([obs.position.x, obs.position.y])))
        
        # 이제 이 하나의 장애물에 대해 위치와 속도를 '동시에' 업데이트
            self.obs_pos = np.array([closest_obs.position.x, closest_obs.position.y])
            self.obs_vel = np.array([closest_obs.velocity.x, closest_obs.velocity.y])
            self.obs_radius = closest_obs.radius


    def in_vo(self, v):

        rel_pos = self.obs_pos - self.drone_pos #이것도 준서랑 논의해야 할 부분, 드론의 절대 위치를 주는 것이 아니라 드론의 위치를 (0,0,0)으로 둔다고 했음.
        rel_vel = v - self.obs_vel

        dist = np.linalg.norm(rel_pos)  #dist:드론과 장애물 사이의 거리
        
        #drone을 점으로 두고, 장애물의 반지름에 드론의 반지름 더해서 점과 원 사이의 충돌로 해석
        combined_radius = self.robot_radius + self.obs_radius 

        if dist < combined_radius:
            return True

        theta = np.arcsin(combined_radius / dist)

        direction = rel_pos / dist #여기에서 하는 것은 단위벡터 두 개의 방향만 비교한다.

        vel_dir = rel_vel / (np.linalg.norm(rel_vel) + 1e-5)

        angle = np.arccos(np.clip(np.dot(direction, vel_dir), -1.0, 1.0))

        return angle < theta
        #더 조건을 주는 것이 좋을 것 같아. angle>theta일 땐 그냥 원래대로 가도록 하고
        #만약에 angle<theta일 땐 여러 후보 속도들을 주어서 선택하여 나아가도록 알고리즘을 짜보자.


    def sample_velocities(self): #속도의 후보를 이따구로 정의하는 게 맞아..? 좀 보완이 필요할 것 같다고 느껴진다.

        samples = []

        for vx in np.linspace(-2, 2, 20):
            for vy in np.linspace(-2, 2, 20):
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

        safe_velocities = []

        for v in candidates: 
            if not self.in_vo(v):
                safe_velocities.append(v)

        if len(safe_velocities) == 0:
            v_safe = np.array([0.0, 0.0])
        else:

            costs = [
                np.linalg.norm(v - self.desired_velocity)
                for v in safe_velocities
            ]

            v_safe = safe_velocities[np.argmin(costs)]

        cmd = Twist()

        cmd.linear.x = float(v_safe[0])
        cmd.linear.y = float(v_safe[1])

        self.cmd_pub.publish(cmd)
        
        #control node에다가 cmd를 전달해주면 된다.
        #VO영역에 들어가있는지 아닌지를 true, false로 계속 vo planner단에서 받아서 vo영역에 있으
        #global planner



def main(args=None):

    rclpy.init(args=args)

    node = VOPlanner()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()