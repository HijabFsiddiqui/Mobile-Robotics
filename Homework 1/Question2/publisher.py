import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class CharPublisherNode(Node):

    def __init__(self):
        super().__init__('char_publisher_node')
        self.publisher_ = self.create_publisher(
            String,
            'char_topic',
            10
        )

    def publish_char(self, character):
        msg = String()
        msg.data = character

        self.publisher_.publish(msg)

        self.get_logger().info(
            'Publishing char: "%s"' % character
        )


def main(args=None):
    rclpy.init(args=args)

    node = CharPublisherNode()

    try:
        while rclpy.ok():
            user_input = input(
                'Enter a character (or "x" to quit): '
            )

            if user_input.lower() == 'x':
                break

            if len(user_input) != 1:
                print('Please enter exactly one character.')
                continue

            node.publish_char(user_input)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
