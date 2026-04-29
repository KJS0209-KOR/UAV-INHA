import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class ControllerNode(Node):

    def __init__(self):
        super().__init__('controller_node')

        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

    def cmd_callback(self, msg):
        v = msg.linear.x
        w = msg.angular.z
        self.get_logger().info(f"Received cmd_vel: v={v}, w={w}")


def main(args=None):   # 🔥 이게 핵심
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()