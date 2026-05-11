#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from rclpy.qos import QoSProfile
from rclpy.qos import ReliabilityPolicy
from rclpy.qos import HistoryPolicy
from rclpy.qos import DurabilityPolicy

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import VehicleCommand
from px4_msgs.msg import VehicleOdometry


class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')

        # ============================================================
        # QoS 설정
        # ============================================================

        # PX4 input topic publisher용 QoS
        px4_pub_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # PX4 output topic subscriber용 QoS
        px4_sub_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.get_logger().info("PX4 Controller Node started.")

        # ============================================================
        # Subscribers
        # ============================================================

        # VO planner에서 계산한 x-y 평면 속도 명령
        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # VO planner가 목표점에 도달했는지 알려주는 topic
        self.create_subscription(
            Bool,
            '/goal_reached',
            self.goal_reached_callback,
            10
        )

        # 현재 드론 위치 확인용
        self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,
            px4_sub_qos
        )

        # ============================================================
        # Publishers
        # ============================================================

        self.offboard_mode_publisher = self.create_publisher(
            OffboardControlMode,
            '/fmu/in/offboard_control_mode',
            px4_pub_qos
        )

        self.trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint,
            '/fmu/in/trajectory_setpoint',
            px4_pub_qos
        )

        self.vehicle_command_publisher = self.create_publisher(
            VehicleCommand,
            '/fmu/in/vehicle_command',
            px4_pub_qos
        )

        # ============================================================
        # Planner command state
        # ============================================================

        # 현재 /cmd_vel은 일반 ROS ENU 속도가 아니라,
        # VO planner가 PX4 odometry 기준으로 계산한 PX4 local x-y 속도라고 가정한다.
        # 따라서 controller에서는 x, y축 변환을 다시 하지 않는다.
        self.v_x = 0.0
        self.v_y = 0.0
        self.v_z = 0.0
        self.yaw_rate = 0.0

        # ============================================================
        # Vehicle state
        # ============================================================

        self.received_odom = False
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_z = 0.0

        # PX4 NED 기준:
        # Gazebo z = +5m 높이
        # PX4 local z = -5m
        self.target_altitude_z = -5.0

        # 고도 유지용 P 제어 gain
        self.altitude_kp = 0.6
        self.max_vertical_speed = 1.0

        # ============================================================
        # Mission state
        # ============================================================

        self.offboard_setpoint_counter = 0
        self.goal_reached = False
        self.land_command_sent = False

        # 상태:
        # INIT_STREAM  : Offboard 진입 전 setpoint stream 공급
        # ARMING       : Offboard mode 전환 + Arm
        # TAKEOFF      : 목표 고도까지 상승
        # MISSION      : VO planner 속도로 이동
        # LANDING      : 착륙 명령 전송 후 대기
        self.state = "INIT_STREAM"

        # 20Hz 제어 주기
        self.timer = self.create_timer(0.05, self.timer_callback)

    # ============================================================
    # Utility
    # ============================================================

    def get_timestamp(self):
        return int(self.get_clock().now().nanoseconds / 1000)

    def clamp(self, value, min_value, max_value):
        return max(min(value, max_value), min_value)

    # ============================================================
    # Callbacks
    # ============================================================

    def cmd_vel_callback(self, msg):
        """
        VO planner에서 /cmd_vel로 들어온 속도 저장.

        중요:
        이 /cmd_vel은 일반적인 ROS ENU 기준 속도가 아니라,
        VOPlanner가 PX4 local x-y 기준으로 계산한 속도라고 가정한다.

        따라서 여기서도 x, y 부호나 축을 바꾸지 않는다.
        """
        self.v_x = msg.linear.x
        self.v_y = msg.linear.y
        self.v_z = msg.linear.z
        self.yaw_rate = msg.angular.z

        self.get_logger().info(
            f"Planner In(PX4 local assumed): "
            f"x={self.v_x:.2f}, y={self.v_y:.2f}, "
            f"z={self.v_z:.2f}, yaw_rate={self.yaw_rate:.2f}"
        )

    def goal_reached_callback(self, msg):
        """
        VO planner가 목표점에 도달했다고 판단하면 true를 publish한다.
        true가 들어오면 controller는 착륙 단계로 전환한다.
        """
        if msg.data and not self.goal_reached:
            self.goal_reached = True
            self.state = "LANDING"
            self.get_logger().info("Goal reached received. Switching to LANDING state.")

    def odom_callback(self, msg):
        """
        PX4 vehicle odometry 기준 현재 위치 저장.

        PX4 local NED 기준:
        z < 0 이면 지면보다 위에 있음.
        예: z = -5.0 → 약 5m 고도
        """
        self.current_x = msg.position[0]
        self.current_y = msg.position[1]
        self.current_z = msg.position[2]

        self.received_odom = True

    # ============================================================
    # PX4 publish functions
    # ============================================================

    def publish_offboard_control_mode(self):
        """
        PX4에게 velocity setpoint 기반 Offboard 제어를 사용할 것이라고 알림.
        Offboard heartbeat 역할도 하므로 Offboard 중에는 계속 publish해야 한다.
        """
        msg = OffboardControlMode()
        msg.timestamp = self.get_timestamp()

        msg.position = False
        msg.velocity = True
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False

        self.offboard_mode_publisher.publish(msg)

    def publish_trajectory_setpoint(self, vx, vy, vz, yawspeed=0.0):
        """
        PX4로 velocity setpoint publish.

        PX4 local frame은 NED 기준:
        - x: North 또는 local x
        - y: East 또는 local y
        - z: Down

        따라서:
        - vz < 0 : 상승
        - vz > 0 : 하강
        """
        msg = TrajectorySetpoint()
        msg.timestamp = self.get_timestamp()

        # velocity 제어만 사용할 것이므로 position은 NaN 처리
        msg.position = [
            float('nan'),
            float('nan'),
            float('nan')
        ]

        msg.velocity = [
            float(vx),
            float(vy),
            float(vz)
        ]

        msg.yawspeed = float(yawspeed)

        self.trajectory_setpoint_publisher.publish(msg)

        self.get_logger().info(
            f"[{self.state}] PX4 Out(NED): "
            f"N={vx:.2f}, E={vy:.2f}, D={vz:.2f}, "
            f"yawspeed={yawspeed:.2f}, "
            f"current_z={self.current_z:.2f}"
        )

    def publish_vehicle_command(self, command, **params):
        """
        PX4 VehicleCommand publish.
        Offboard 모드 전환, Arm, Land 등에 사용한다.
        """
        msg = VehicleCommand()
        msg.timestamp = self.get_timestamp()

        msg.command = command

        msg.param1 = float(params.get("param1", 0.0))
        msg.param2 = float(params.get("param2", 0.0))
        msg.param3 = float(params.get("param3", 0.0))
        msg.param4 = float(params.get("param4", 0.0))
        msg.param5 = float(params.get("param5", 0.0))
        msg.param6 = float(params.get("param6", 0.0))
        msg.param7 = float(params.get("param7", 0.0))

        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True

        self.vehicle_command_publisher.publish(msg)

    def engage_offboard_mode(self):
        """
        PX4 Offboard 모드 전환 명령.

        param1 = 1.0 : custom mode 사용
        param2 = 6.0 : PX4 custom main mode Offboard
        """
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_DO_SET_MODE,
            param1=1.0,
            param2=6.0
        )

        self.get_logger().info("Offboard mode command sent.")

    def arm(self):
        """
        PX4 Arm 명령.
        """
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,
            param1=1.0
        )

        self.get_logger().info("Arm command sent.")

    def land(self):
        """
        PX4 Land 명령.

        목표점 도달 후 이 명령을 보내면 PX4가 착륙 모드로 전환된다.
        """
        self.publish_vehicle_command(
            VehicleCommand.VEHICLE_CMD_NAV_LAND
        )

        self.land_command_sent = True
        self.get_logger().info("Land command sent.")

    # ============================================================
    # Control helpers
    # ============================================================

    def compute_altitude_hold_vz(self):
        """
        목표 고도 z = -5.0 근처를 유지하기 위한 z속도 계산.

        PX4 NED 기준에서:
        error_z = target_z - current_z

        예:
        current_z = -3, target_z = -5
        error_z = -2
        vz < 0 이므로 상승

        current_z = -6, target_z = -5
        error_z = +1
        vz > 0 이므로 하강
        """
        if not self.received_odom:
            return 0.0

        error_z = self.target_altitude_z - self.current_z
        vz_cmd = self.altitude_kp * error_z

        vz_cmd = self.clamp(
            vz_cmd,
            -self.max_vertical_speed,
            self.max_vertical_speed
        )

        return vz_cmd

    # ============================================================
    # Main timer loop
    # ============================================================

    def timer_callback(self):
        """
        전체 제어 루프.

        INIT_STREAM:
            Offboard 진입 전 PX4가 setpoint stream을 인식하도록 1초 정도 setpoint 전송

        ARMING:
            Offboard 모드 전환 + Arm

        TAKEOFF:
            PX4 local z = -5.0 근처까지 상승

        MISSION:
            VO planner의 x-y 속도를 그대로 사용하고, z는 -5.0 근처로 유지

        LANDING:
            /goal_reached 수신 후 PX4에 Land command 전송
        """

        # 착륙 상태에서는 더 이상 Offboard setpoint를 강하게 밀지 않는다.
        if self.state == "LANDING":
            if not self.land_command_sent:
                self.land()
            return

        # Offboard 중에는 heartbeat를 계속 보낸다.
        self.publish_offboard_control_mode()

        # ------------------------------------------------------------
        # Phase 1. Offboard 진입 전 setpoint stream 공급
        # ------------------------------------------------------------
        if self.state == "INIT_STREAM":
            self.publish_trajectory_setpoint(
                vx=0.0,
                vy=0.0,
                vz=0.0,
                yawspeed=0.0
            )

            self.offboard_setpoint_counter += 1

            if self.offboard_setpoint_counter >= 20:
                self.state = "ARMING"

            return

        # ------------------------------------------------------------
        # Phase 2. Offboard 모드 전환 + Arm
        # ------------------------------------------------------------
        if self.state == "ARMING":
            self.engage_offboard_mode()
            self.arm()

            self.state = "TAKEOFF"
            return

        # ------------------------------------------------------------
        # Phase 3. Takeoff
        # ------------------------------------------------------------
        if self.state == "TAKEOFF":
            # odometry가 아직 없으면 일단 상승 명령
            if not self.received_odom:
                self.publish_trajectory_setpoint(
                    vx=0.0,
                    vy=0.0,
                    vz=-0.8,
                    yawspeed=0.0
                )
                return

            # 목표 고도에 가까워질 때까지 상승
            if self.current_z > self.target_altitude_z + 0.3:
                self.publish_trajectory_setpoint(
                    vx=0.0,
                    vy=0.0,
                    vz=-0.8,
                    yawspeed=0.0
                )
                return

            # 목표 고도 도달
            self.get_logger().info(
                f"Takeoff complete. current_z={self.current_z:.2f}. Switching to MISSION."
            )
            self.state = "MISSION"
            return

        # ------------------------------------------------------------
        # Phase 4. Mission
        # ------------------------------------------------------------
        if self.state == "MISSION":
            vz_hold = self.compute_altitude_hold_vz()

            # 현재 /cmd_vel은 이미 PX4 local x-y 기준이라고 가정한다.
            # 따라서 여기서 x/y 축 변환 또는 부호 반전을 하지 않는다.
            self.publish_trajectory_setpoint(
                vx=self.v_x,
                vy=self.v_y,
                vz=vz_hold,
                yawspeed=self.yaw_rate
            )

            return


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