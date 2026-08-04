import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from robot_controller.yahboom_motor import drive_forward, drive_backward, stop_robot


class MotorNode(Node):

    def __init__(self):
        super().__init__('motor_node')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

    def cmd_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        MAX_SPEED = 600
        speed = int(abs(linear) * MAX_SPEED)

        print(f"Linear: {linear:.2f}, Angular: {angular:.2f}")

        if linear > 0.05:
            drive_forward(speed)
k
        elif linear < -0.05:
            drive_backward(speed)

        else:
            stop_robot()
        

def main(args=None):

    rclpy.init(args=args)

    node = MotorNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
