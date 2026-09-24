from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(package='turtle_py_pkg', executable='turtle_sim_poses',
             name='turtle_sim_poses'),
        Node(package='turtle_py_pkg', executable='turtle_tf2_listener',
             name='turtle_tf2_listener', output='screen'),
    ])

