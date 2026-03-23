#!/usr/bin/env python3

"""
obstacle_state_publisher
--------------------------------------------
입력 : /model/cylinder_obstacle_1/pose_static
    - 타입 : TransformStamped
출력 : /obstacle_states
    - 타입 : ObstacleArray
=> 특정 장애물 선택하여, Gazebo -> PX4 좌표 변환 및 ObstacleState 채우고 배열에 담아서 publish
--------------------------------------------
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy

from geometry_msgs.msg import TransformStamped
from uav_interfaces.msg import Obstacle, ObstacleArray


class ObstacleStatePublisher(Node):

    def __init__(self):
        super().__init__('obstacle_state_publisher')

        self.obstacles = {}
        self.prev_positions = {}
        self.prev_times = {}

        obstacle_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.VOLATILE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )

        # obstacle별 설정
        self.obstacle_configs = {
            "cylinder_obstacle_1": {
                "pose_type": "pose_static",
                "radius": 1.8,
                "height": 6.0,
                "is_static": True,
            },
            "cylinder_obstacle_2": {
                "pose_type": "pose_static",
                "radius": 1.8,
                "height": 6.0,
                "is_static": True,
            },
            "cylinder_obstacle_3": {
                "pose_type": "pose_static",
                "radius": 3.0,   # 실제 반지름 2.5 + margin
                "height": 8.0,
                "is_static": True,
            },
            "moving_obstacle_1": {
                "pose_type": "pose",
                "radius": 3.5,   # sphere radius 3.0 + margin
                "height": 0.0,
                "is_static": False,
            },
        }

        self.obstacle_subscriptions = []

        for obstacle_name, config in self.obstacle_configs.items():
            topic_name = f"/model/{obstacle_name}/{config['pose_type']}"

            sub = self.create_subscription(
                TransformStamped,
                topic_name,
                lambda msg, name=obstacle_name: self.obstacle_callback(msg, name),
                obstacle_qos
            )
            self.obstacle_subscriptions.append(sub)
            self.get_logger().info(f"Subscribed to {topic_name}")

        self.publisher_ = self.create_publisher(
            ObstacleArray,
            "/obstacle_states",
            10
        )

        self.timer = self.create_timer(0.1, self.publish_obstacle_array)

        self.get_logger().info("ObstacleStatePublisher started")

    def obstacle_callback(self, msg: TransformStamped, obstacle_name: str):
        if msg.child_frame_id != obstacle_name:
            return

        config = self.obstacle_configs[obstacle_name]

        # Gazebo -> PX4
        gz_x = msg.transform.translation.x
        gz_y = msg.transform.translation.y
        gz_z = msg.transform.translation.z

        px4_x = gz_y
        px4_y = gz_x
        px4_z = -gz_z

        # velocity 계산
        now = self.get_clock().now().nanoseconds * 1e-9
        vx, vy, vz = 0.0, 0.0, 0.0

        if not config["is_static"]:
            if obstacle_name in self.prev_positions:
                prev_x, prev_y, prev_z = self.prev_positions[obstacle_name]
                prev_t = self.prev_times[obstacle_name]
                dt = now - prev_t

                if dt > 1e-6:
                    vx = (px4_x - prev_x) / dt
                    vy = (px4_y - prev_y) / dt
                    vz = (px4_z - prev_z) / dt

            self.prev_positions[obstacle_name] = (px4_x, px4_y, px4_z)
            self.prev_times[obstacle_name] = now

        obstacle = Obstacle()
        obstacle.id = obstacle_name

        obstacle.position.x = px4_x
        obstacle.position.y = px4_y
        obstacle.position.z = px4_z

        obstacle.velocity.x = vx
        obstacle.velocity.y = vy
        obstacle.velocity.z = vz

        obstacle.radius = config["radius"]
        obstacle.height = config["height"]
        obstacle.is_static = config["is_static"]
        obstacle.is_valid = True
        obstacle.confidence = 1.0
        obstacle.source_type = "gazebo_gt"

        self.obstacles[obstacle_name] = obstacle

    def publish_obstacle_array(self):
        obstacle_array = ObstacleArray()

        obstacle_array.header.stamp = self.get_clock().now().to_msg()
        obstacle_array.header.frame_id = "px4_local"

        for obstacle_name in sorted(self.obstacles.keys()):
            obstacle_array.obstacles.append(self.obstacles[obstacle_name])

        self.publisher_.publish(obstacle_array)


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