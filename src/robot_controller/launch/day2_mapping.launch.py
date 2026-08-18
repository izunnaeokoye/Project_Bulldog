from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        # LiDAR
        Node(
            package='oradar_lidar',
            executable='oradar_scan',
            name='MS200',
            output='screen',
            parameters=[
                {'device_model': 'MS200'},
                {'frame_id': 'laser_frame'},
                {'scan_topic': 'MS200/scan'},
                {'port_name': '/dev/lidar'},
                {'baudrate': 230400},
                {'angle_min': 0.0},
                {'angle_max': 360.0},
                {'range_min': 0.05},
                {'range_max': 20.0},
                {'clockwise': False},
                {'motor_speed': 10}
            ]
        ),

        # Odometry
        Node(
            package='robot_controller',
            executable='odom_node',
            name='odom_node',
            output='screen'
        ),

        # Motor controller
        Node(
            package='robot_controller',
            executable='motor_node',
            name='motor_node',
            output='screen'
        ),

        # base_link -> laser_frame
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_base_laser',
            arguments=[
                '0', '0', '0.18',
                '0', '0', '0',
                'base_link',
                'laser_frame'
            ],
            output='screen'
        ),

        # SLAM Toolbox
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                {
                    'solver_plugin': 'solver_plugins::CeresSolver',
                    'odom_frame': 'odom',
                    'map_frame': 'map',
                    'base_frame': 'base_link',
                    'scan_topic': '/MS200/scan',
                    'mode': 'mapping',
                    'use_scan_matching': True,
                    'use_scan_barycenter': True,
                    'minimum_travel_distance': 0.5,
                    'minimum_travel_heading': 0.5,
                    'resolution': 0.05,
                    'map_update_interval': 5.0,
                    'transform_publish_period': 0.02,
                    'max_laser_range': 20.0,
                    'minimum_time_interval': 0.5,
                    'transform_timeout': 0.2,
                    'tf_buffer_duration': 30.0,
                    'stack_size_to_use': 40000000,
                    'do_loop_closing': True
                }
            ]
        )

    ])
