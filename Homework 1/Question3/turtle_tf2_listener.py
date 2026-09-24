import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):
    def __init__(self):
        super().__init__('turtle_tf2_frame_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_timer(0.5, self.on_timer)

    def on_timer(self):
        try:
            t = self.tf_buffer.lookup_transform('turtleA', 'turtleB', rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(f'Could not transform: {ex}')
            return
        x, y = t.transform.translation.x, t.transform.translation.y
        q = t.transform.rotation
        yaw = 2 * math.atan2(q.z, q.w)
        self.get_logger().info(
            f'B in A: x={x:.2f} y={y:.2f} yaw={yaw:.2f} dist={math.hypot(x, y):.2f}')


def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == '__main__':
    main()
