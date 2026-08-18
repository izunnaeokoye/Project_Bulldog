import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from robot_controller.yahboom_motor import send_wheel_speeds, stop_robot


class MotorNode(Node):

    def __init__(self):
        super().__init__('motor_node')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.get_logger().info('Motor node started')

    def cmd_callback(self, msg):

        linear = msg.linear.x
        angular = msg.angular.z

        MAX_SPEED = 400

        # Differential-drive mixing
        left = (linear - angular) * MAX_SPEED
        right = (linear + angular) * MAX_SPEED

        # Limit speeds
        left = max(min(left, MAX_SPEED), -MAX_SPEED)
        right = max(min(right, MAX_SPEED), -MAX_SPEED)

        # Convert logical wheel directions into
        # the physical motor directions used by the Yahboom board.
        send_wheel_speeds({
            "front_left": int(left),
            "rear_left": int(-left),
            "front_right": int(right),
            "rear_right": int(-right),
        })

    def destroy_node(self):
        stop_robot()
        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = MotorNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
