import os
from setuptools import find_packages, setup

package_name = 'robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
    (os.path.join('share', package_name, 'config'), ['config/bulldog_slam.yaml']),
    (os.path.join('share', package_name, 'launch'),
        ['launch/day2_mapping.launch.py']),
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='izunna',
    maintainer_email='izunna@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
	'motor_node = robot_controller.motor_node:main',
	'odom_node = robot_controller.odom_node:main'
        ],
    },
)
