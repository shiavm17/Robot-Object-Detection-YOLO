import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'robot_object_detection_yolo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'models'), glob('models/*.pt')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shivam',
    maintainer_email='shivamchaturvedi.in@gmail.com',
    description='YOLOv8 object detection node for ROS2 mobile robots',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'detector_node = robot_object_detection_yolo.detector_node:main',
        ],
    },
)
