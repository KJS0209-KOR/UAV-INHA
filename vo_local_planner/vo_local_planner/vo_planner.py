import rclpy
from rclpy.node import Node

#ROS 토픽은 그냥 데이터가 아니라 정해진 메시지 타입을 사용합니다.
#Python 코드에서 이 타입을 사용하려면 import를 해야 합니다.
#geometry_msgs에 어떤 메시지 타입들이 존재하는지 알아야 한다.
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry #드론의 위치, 속도를 받는 메시지 관련 토픽
#UBUNTU 들어가서 어떤 메시지 타입이 있는지 다 봐야해!!!




import numpy as np


class VOPlanner(Node):

    def __init__(self):
        super().__init__('vo_planner')

        # drone pose, 메시지 받기 전에 0으로 초기화하는 작업
        self.drone_pos = np.array([0.0, 0.0])
        self.drone_vel = np.array([0.0, 0.0])

        # obstacle pose
        self.obs_pos = np.array([0.0, 0.0])
        self.obs_vel = np.array([0.0, 0.0])

        # robot / obstacle radius
        self.robot_radius = 0.5 #0.4~0.5 사이에서 조절을 해보자.
        self.obs_radius = 3 #장애물의 크기도 받아서 바꾸자.

        # 목표 속도
        self.desired_velocity = np.array([1.0, 0.0])

        # subscriber, drone pose를 받는다. from gazebo topic
        self.create_subscription(
            PoseStamped,
            '/drone_pose',
            self.drone_callback,
            10
        )
        
        #장애물의 속도 subscribe하기
        self.twist_sub = self.create_subscription(
            Twist,
            '/model/moving_obstacle_1/twist',
            self.twist_callback,
            10)

        self.pose = None
        self.vel = None

        self.create_subscription( #장애물의 pose를 받는다.
            PoseStamped,
            '/obstacle_pose',
            self.obstacle_callback,
            10
        )

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
            msg.pose.position.x,
            msg.pose.position.y
        ])


    def obstacle_callback(self, msg): #장애물 위치를 받는 함수
        self.obs_pos = np.array([
            msg.pose.position.x,
            msg.pose.position.y
        ])


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