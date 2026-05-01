import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import numpy as np # NaN 처리를 위해 추가

# 메시지 타입들
from geometry_msgs.msg import Twist
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')

        # 1. PX4 통신용 QoS (에이전트 호환용)
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.get_logger().info("PX4 Controller Node has been started.")

        # 2. 구독자: 플래너(/cmd_vel)로부터 속도 수신
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        # 3. 발행자: PX4로 명령 전달
        self.offboard_mode_publisher = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)

        # 변수 초기화 (플래너의 모든 축 수용)
        self.v_x = 0.0
        self.v_y = 0.0
        self.v_z = 0.0
        self.yaw_rate = 0.0
        
        # 10Hz(0.1초) 주기로 명령 실행
        self.timer = self.create_timer(0.05, self.timer_callback)

    def cmd_vel_callback(self, msg):
        """플래너로부터 받은 속도 저장"""
        self.v_x = msg.linear.x
        self.v_y = msg.linear.y
        self.v_z = msg.linear.z
        self.yaw_rate = msg.angular.z
        self.get_logger().info(f"Received cmd_vel: x={self.v_x}, y={self.v_y}, z={self.v_z}")

    def timer_callback(self):
        """주기적으로 PX4에 명령 하달"""
        timestamp = int(self.get_clock().now().nanoseconds / 1000)

        # [1] Offboard 모드 Heartbeat
        offboard_msg = OffboardControlMode()
        offboard_msg.position = False
        offboard_msg.velocity = True  # 속도 제어 활성화
        offboard_msg.acceleration = False
        offboard_msg.timestamp = timestamp
        self.offboard_mode_publisher.publish(offboard_msg)

        # [2] 실제 속도 명령 (TrajectorySetpoint)
        setpoint_msg = TrajectorySetpoint()
        setpoint_msg.timestamp = timestamp
        
        # 중요: 위치 제어를 사용하지 않을 때는 position 값을 float('nan')으로 채워야
        # PX4 내부의 위치 제어기랑 충돌하지 않습니다.
        setpoint_msg.position = [float('nan'), float('nan'), float('nan')]
        
        # 플래너에서 받은 속도 적용
        setpoint_msg.velocity = [self.v_x, self.v_y, self.v_z]
        setpoint_msg.yawspeed = self.yaw_rate
        
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