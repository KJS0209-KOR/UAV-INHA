#!/usr/bin/env python3

"""
obstacle_state_publisher
--------------------------------------------
입력 : /model/cylinder_obstacle_1/pose_static
    - 타입 : TransformStamped
출력 : /obstacle_states
    - 타입 : ObstacleStateArray
=> 특정 장애물 선택하여, Gazebo -> PX4 좌표 변환 및 ObstacleState 채우고 배열에 담아서 publish
--------------------------------------------
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy

from geometry_msgs.msg import TransformStamped  # Gazebo bridge에서 오는 장애물 pose
from uav_interfaces.msg import Obstacle, ObstacleArray  # 직접 만든 장애물 state 메시지


class ObstacleStatePublisher(Node):

    def __init__(self):
        super().__init__('obstacle_state_publisher')

        obstacle_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.VOLATILE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.target_obstacle = 'cylinder_obstacle_1'

        self.publisher_ = self.create_publisher(
            ObstacleArray,
            '/obstacle_states',
            10
        )

        self.subscription = self.create_subscription(
            TransformStamped,
            '/model/cylinder_obstacle_1/pose_static',
            self.obstacle_callback,
            obstacle_qos
        )

        self.get_logger().info('ObstacleStatePublisher started')

        self.safety_radius = 1.8

    def obstacle_callback(self, msg: TransformStamped):
        if msg.child_frame_id != self.target_obstacle:
            return

        gz_x = msg.transform.translation.x
        gz_y = msg.transform.translation.y
        gz_z = msg.transform.translation.z

        px4_x = gz_y
        px4_y = gz_x
        px4_z = -gz_z

        obstacle = Obstacle()
        obstacle.id = self.target_obstacle

        obstacle.position.x = px4_x
        obstacle.position.y = px4_y
        obstacle.position.z = px4_z

        obstacle.velocity.x = 0.0
        obstacle.velocity.y = 0.0
        obstacle.velocity.z = 0.0

        obstacle.radius = self.safety_radius
        obstacle.height = 0.0
        obstacle.is_static = True
        obstacle.is_valid = True
        obstacle.confidence = 1.0
        obstacle.source_type = 'gazebo_gt'

        obstacle_array = ObstacleArray()
        obstacle_array.obstacles.append(obstacle)

        self.publisher_.publish(obstacle_array)

        self.get_logger().info(
            f'Published obstacle: id={obstacle.id}, '
            f'pos=({obstacle.position.x:.2f}, {obstacle.position.y:.2f}, {obstacle.position.z:.2f}), '
            f'radius={obstacle.radius:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleStatePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
