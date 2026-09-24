import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
import time


topic_name = 'turtle1/cmd_vel'


class CosineWaveNode(Node):

    def __init__(self):
        super().__init__('cosine_wave_node')

        self.publisher = self.create_publisher(
            Twist,
            topic_name,
            10
        )

        self.timer = self.create_timer(
            0.05,
            self.publish_velocity
        )

        self.start_time = time.time()

    def publish_velocity(self):
        t = time.time() - self.start_time

        msg = Twist()
        msg.linear.x = 0.5
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        # msg.angular.z = -2.0 * math.sin(2.0 * t)
        msg.angular.z = 2.0 * math.cos(2.0 * t + math.pi / 2)

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = CosineWaveNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()