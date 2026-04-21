import os

from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('g1_description')
    
    # Path to files
    urdf_file = os.path.join(pkg_share, 'urdf', 'robot.urdf')
    controllers_file = os.path.join(pkg_share, 'config', 'controllers.yaml')

    # robot_description
    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()
    
    robot_description = {'robot_description': robot_description_content}

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description],
    )

    # Controller Manager (Standalone for mock testing)
    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, controllers_file],
        output='both',
    )
    
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
    )

    g1_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['g1_controller'],
        output='screen',
    )

    # Delay loading g1_controller until joint_state_broadcaster is up
    delay_g1_controller_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[g1_controller_spawner],
        )
    )


    rviz_config_file = os.path.join(pkg_share, 'rviz', 'default.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        controller_manager_node,
        joint_state_broadcaster_spawner,
        delay_g1_controller_spawner,
        rviz_node,
    ])
