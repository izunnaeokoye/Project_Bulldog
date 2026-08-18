import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster


class OdomNode(Node):

    def __init__(self):
        super().__init__('odom_node')

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

        self.last_time = self.get_clock().now()
        self.last_cmd_time = self.get_clock().now()

        self.cmd_subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.odom_publisher = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        self.tf_broadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(
            1.0 / 30.0,
            self.update_odom
        )

        self.get_logger().info('Open-loop odometry started')

    def cmd_callback(self, msg):
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z
        self.last_cmd_time = self.get_clock().now()

    def update_odom(self):
        current_time = self.get_clock().now()

        dt = (
            current_time - self.last_time
        ).nanoseconds / 1e9

        self.last_time = current_time

        if dt <= 0.0 or dt > 1.0:
            return

        # Stop integrating if no command has been received
        # for more than 0.5 seconds.
        time_since_cmd = (
            current_time - self.last_cmd_time
        ).nanoseconds / 1e9

        if time_since_cmd > 0.5:
            self.linear_velocity = 0.0
            self.angular_velocity = 0.0

        # Integrate velocity
        self.x += (
            self.linear_velocity
            * math.cos(self.theta)
            * dt
        )

        self.y += (
            self.linear_velocity
            * math.sin(self.theta)
            * dt
        )

        self.theta += self.angular_velocity * dt

        # Normalize angle to [-pi, pi]
        self.theta = math.atan2(
            math.sin(self.theta),
            math.cos(self.theta)
        )

        # Convert yaw to quaternion
        qz = math.sin(self.theta / 2.0)
        qw = math.cos(self.theta / 2.0)

        # Publish Odometry
        odom = Odometry()

        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        odom.twist.twist.linear.x = self.linear_velocity
        odom.twist.twist.angular.z = self.angular_velocity

        self.odom_publisher.publish(odom)

        # Publish odom -> base_link TF
        transform = TransformStamped()

        transform.header.stamp = current_time.to_msg()
        transform.header.frame_id = 'odom'
        transform.child_frame_id = 'base_link'

        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.translation.z = 0.0

        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(transform)


def main(args=None):
    rclpy.init(args=args)

    node = OdomNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
