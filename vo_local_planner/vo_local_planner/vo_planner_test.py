import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VOPlannerTest(Node):

    def __init__(self):
        super().__init__('vo_planner_test')

        # /cmd_vel 퍼블리셔
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # 0.1초마다 실행
        self.timer = self.create_timer(
            0.1,
            self.publish_cmd
        )

    def publish_cmd(self):
        cmd = Twist()

        # 👉 그냥 앞으로 가라는 명령
        cmd.linear.x = 0.5
        cmd.linear.y=0.0
        cmd.linear.z=0.0
        cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)

        self.get_logger().info(f'Publishing cmd_vel: {cmd.linear.x}')


def main(args=None):
    rclpy.init(args=args)

    node = VOPlannerTest()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()