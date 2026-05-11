from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    cylinder_obstacle_1_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='cylinder_obstacle_1_pose_static_bridge',
        arguments=[
            '/model/cylinder_obstacle_1/pose_static'
            + '@geometry_msgs/msg/TransformStamped'
            + '[gz.msgs.Pose'
        ],
        output='screen'
    )

    cylinder_obstacle_2_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='cylinder_obstacle_2_pose_static_bridge',
        arguments=[
            '/model/cylinder_obstacle_2/pose_static'
            + '@geometry_msgs/msg/TransformStamped'
            + '[gz.msgs.Pose'
        ],
        output='screen'
    )

    cylinder_obstacle_3_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='cylinder_obstacle_3_pose_static_bridge',
        arguments=[
            '/model/cylinder_obstacle_3/pose_static'
            + '@geometry_msgs/msg/TransformStamped'
            + '[gz.msgs.Pose'
        ],
        output='screen'
    )

    moving_obstacle_1_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='moving_obstacle_1_pose_bridge',
        arguments=[
            '/model/moving_obstacle_1/pose'
            + '@geometry_msgs/msg/TransformStamped'
            + '[gz.msgs.Pose'
        ],
        output='screen'
    )

    obstacle_state_publisher = Node(
        package='obstacle_state_publisher',
        executable='obstacle_state_publisher',
        name='obstacle_state_publisher',
        output='screen'
    )

    return LaunchDescription([
        cylinder_obstacle_1_bridge,
        cylinder_obstacle_2_bridge,
        cylinder_obstacle_3_bridge,
        moving_obstacle_1_bridge,
        obstacle_state_publisher,
    ])