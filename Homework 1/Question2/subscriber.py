import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CharSubscriberNode(Node):

    def __init__(self):
        super().__init__('char_subscriber_node')
        self.subscriber_ = self.create_subscription(
            String,
            'char_topic',
            self.callbackFunction,
            10
        )
        self.subscriber_  # prevent unused variable warning

    def callbackFunction(self, msg):
        received_char = msg.data
        self.get_logger().info('Received char: "%s"' % received_char)


def main(args=None):
    rclpy.init(args=args)
    node = CharSubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()