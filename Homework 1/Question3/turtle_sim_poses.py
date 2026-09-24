import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from turtlesim.srv import Spawn, TeleportAbsolute

CX, CY = 5.5, 5.5      # turtlesim window centre / world origin
B_PERIOD = 10.0        # restart B's path every B_PERIOD seconds so it stays in the window


class TurtleSimPoses(Node):
    def __init__(self):
        super().__init__('turtle_sim_poses')
        self.br = TransformBroadcaster(self)

        self.tpA = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.tpB = self.create_client(TeleportAbsolute, '/turtle2/teleport_absolute')
        spawn = self.create_client(Spawn, '/spawn')

        spawn.wait_for_service()
        req = Spawn.Request()
        req.x, req.y, req.theta, req.name = CX, CY, 0.0, 'turtle2'
        spawn.call_async(req)

        self.tpA.wait_for_service()
        self.tpB.wait_for_service()

        self.t0 = self.get_clock().now()
        self.timer = self.create_timer(0.05, self.on_timer)  # 20 Hz

    def on_timer(self):
        t = (self.get_clock().now() - self.t0).nanoseconds * 1e-9

        # Robot A: circle
        R, w = 5.0, 0.4
        xA, yA = R * math.cos(w * t), R * math.sin(w * t)
        thA = w * t + math.pi / 2

        # Robot B: sine wave
        L, a, T = 5.0, 1.0, 8.0
        tb = t % B_PERIOD
        s = math.sin(2 * math.pi * tb / T)
        c = math.cos(2 * math.pi * tb / T)
        xB = -(L * tb / T + a * s) / math.sqrt(2)
        yB = (L * tb / T - a * s) / math.sqrt(2)
        thB = math.atan2(L - 2 * math.pi * a * c, -L - 2 * math.pi * a * c)

        # TF in the un-shifted world frame
        self.publish_tf('world', 'turtleA', xA, yA, thA)
        self.publish_tf('world', 'turtleB', xB, yB, thB)

        # Turtlesim display, shifted to window centre
        self.teleport(self.tpA, xA + CX, yA + CY, thA)
        self.teleport(self.tpB, xB + CX, yB + CY, thB)

    def teleport(self, client, x, y, th):
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = x, y, th
        client.call_async(req)

    def publish_tf(self, parent, child, x, y, theta):
        m = TransformStamped()
        m.header.stamp = self.get_clock().now().to_msg()
        m.header.frame_id = parent
        m.child_frame_id = child
        m.transform.translation.x = x
        m.transform.translation.y = y
        m.transform.translation.z = 0.0
        m.transform.rotation.z = math.sin(theta / 2)
        m.transform.rotation.w = math.cos(theta / 2)
        self.br.sendTransform(m)


def main():
    rclpy.init()
    node = TurtleSimPoses()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
