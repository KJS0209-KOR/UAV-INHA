import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import numpy as np

# 메시지 타입들
from geometry_msgs.msg import Twist
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')

        # 1. PX4 통신용 QoS (Best Effort & Volatile)
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.get_logger().info("PX4 Controller Node with Frame Conversion started.")

        # 2. 구독자: 플래너(/cmd_vel)로부터 속도 수신
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        # 3. 발행자: PX4로 명령 전달
        self.offboard_mode_publisher = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)

        # 변수 초기화
        self.v_x = 0.0 # Forward
        self.v_y = 0.0 # Left
        self.v_z = 0.0 # Up
        self.yaw_rate = 0.0
        
        # 20Hz(0.05초) 주기로 명령 실행 (안정적인 Offboard 전환을 위해 20Hz 권장)
        self.timer = self.create_timer(0.05, self.timer_callback)

    def cmd_vel_callback(self, msg):
        """플래너(ROS ENU 기준)로부터 받은 속도 저장"""
        self.v_x = msg.linear.x
        self.v_y = msg.linear.y
        self.v_z = msg.linear.z
        self.yaw_rate = msg.angular.z

    def timer_callback(self):
        """주기적으로 PX4(NED 기준)에 명령 하달"""
        timestamp = int(self.get_clock().now().nanoseconds / 1000)

        # [1] Offboard 모드 Heartbeat
        offboard_msg = OffboardControlMode()
        offboard_msg.timestamp = timestamp
        offboard_msg.position = False
        offboard_msg.velocity = True
        offboard_msg.acceleration = False
        offboard_msg.attitude = False
        offboard_msg.body_rate = False
        self.offboard_mode_publisher.publish(offboard_msg)

        # [2] 실제 속도 명령 (TrajectorySetpoint)
        setpoint_msg = TrajectorySetpoint()
        setpoint_msg.timestamp = timestamp
        
        # 위치 제어 미사용 시 NaN 처리
        setpoint_msg.position = [float('nan'), float('nan'), float('nan')]
        
        # 🚀 [핵심] ROS ENU -> PX4 NED 좌표 변환
        # ROS X (Forward) -> PX4 X (North/Forward)
        # ROS Y (Left)    -> PX4 Y (East/Right) 를 맞추기 위해 부호 반전 (-Y)
        # ROS Z (Up)      -> PX4 Z (Down) 를 맞추기 위해 부호 반전 (-Z)
        setpoint_msg.velocity = [
            self.v_x,      # PX4 North = ROS Forward
            -self.v_y,     # PX4 East = ROS Right (Left의 반대)
            -self.v_z      # PX4 Down = ROS Down (Up의 반대)
        ]
        
        # Yaw Rate 또한 방향 반전 (ROS는 반시계방향 +, PX4는 시계방향 +)
        setpoint_msg.yawspeed = -self.yaw_rate 
        
        self.trajectory_setpoint_publisher.publish(setpoint_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()