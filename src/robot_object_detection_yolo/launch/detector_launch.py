import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('robot_object_detection_yolo')
    default_model_path = os.path.join(pkg_share, 'models', 'yolov8n.pt')

    camera_topic_arg = DeclareLaunchArgument(
        'camera_topic',
        default_value='/camera/image_raw',
        description='Camera topic to subscribe to'
    )

    model_path_arg = DeclareLaunchArgument(
        'model_path',
        default_value=default_model_path,
        description='Path to YOLOv8 model weights'
    )

    confidence_arg = DeclareLaunchArgument(
        'confidence_threshold',
        default_value='0.5',
        description='Minimum confidence for detections'
    )

    detector_node = Node(
        package='robot_object_detection_yolo',
        executable='detector_node',
        name='yolo_detector_node',
        output='screen',
        parameters=[{
            'camera_topic': LaunchConfiguration('camera_topic'),
            'model_path': LaunchConfiguration('model_path'),
            'confidence_threshold': LaunchConfiguration('confidence_threshold'),
        }]
    )

    return LaunchDescription([
        camera_topic_arg,
        model_path_arg,
        confidence_arg,
        detector_node
    ])
