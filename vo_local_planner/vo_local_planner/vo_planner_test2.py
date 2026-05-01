import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import numpy as np

from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint

class VOPlannerTest(Node):
    def __init__(self):
        super().__init__('vo_planner_test')

        # PX4 통신을 위한 QoS 설정
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # 퍼블리셔 설정
        self.offboard_ctrl_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)

        # 0.1초마다 실행
        self.timer = self.create_timer(0.1, self.publish_cmd)

        # 목표 방향 설정 (예: 90도 = PI/2 라디안)
        self.target_yaw = 1.57

    def publish_cmd(self):
        # [A] Offboard 제어 모드 설정
        offboard_msg = OffboardControlMode()
        offboard_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        offboard_msg.position = False
        offboard_msg.velocity = True
        offboard_msg.acceleration = False
        offboard_msg.attitude = False
        offboard_msg.body_rate = False
        self.offboard_ctrl_pub.publish(offboard_msg)

        # [B] 목표치 설정 (속도 + 방향)
        setpoint_msg = TrajectorySetpoint()
        setpoint_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)

        # 1. 속도 설정 (NED 좌표계: x=전진, y=오른쪽, z=아래)
        setpoint_msg.velocity = [0.5, 0.0, 0.0]

        # 2. 방향(Orientation) 설정
        setpoint_msg.yaw = self.target_yaw  # 특정 각도를 바라보게 함
        
        self.trajectory_pub.publish(setpoint_msg)
        self.get_logger().info(f'Publishing Velocity: 0.5, Yaw: {setpoint_msg.yaw} rad')

def main(args=None):
    rclpy.init(args=args)
    node = VOPlannerTest()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()