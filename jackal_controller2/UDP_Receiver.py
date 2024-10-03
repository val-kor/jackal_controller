import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket

# Set up the UDP IP and port for communication
UDP_IP = '0.0.0.0'
UDP_PORT = 5007
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.1)  # Set a timeout of 0.1 seconds for non-blocking behavior


class CmdPublisher(Node):
    def __init__(self):
        super().__init__('command_publisher')
        self.pub_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.commandCallback)
        self.cmd = 0  # Initial command value (could be treated as stop)

    def commandCallback(self):
        twist = Twist()

        try:
            # Try to receive data without blocking
            data, addr = sock.recvfrom(1024)
            print(f"Received {data}")
            self.cmd = int(format(data[0], '04b'))
            print(f"After formatting: {self.cmd}")
        except socket.timeout:
            # No new data received, keep using the previous command
            print("No new command received, using the previous command.")

        # Based on the last command, update the twist message
        if self.cmd == 1: 
            twist.linear.x = 0.5
            twist.angular.z = 0.0
        elif self.cmd == 10:  # Move backward
            twist.linear.x = -0.5
            twist.angular.z = 0.0
        elif self.cmd == 100:  # Turn left
            twist.linear.x = 0.0
            twist.angular.z = -1.0
        elif self.cmd == 1000:  # Turn right
            twist.linear.x = 0.0
            twist.angular.z = 1.0
        elif self.cmd == 0:  # Stop
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        else:
            self.get_logger().info(f'Unknown command: {self.cmd}')
            return
      
            

        # Continue publishing the last or updated twist message
        print("Ready to publish")
        self.pub_.publish(twist)
        print(f"Command has been published: {self.cmd}")


def main(args=None):
    rclpy.init(args=args)
    node = CmdPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
