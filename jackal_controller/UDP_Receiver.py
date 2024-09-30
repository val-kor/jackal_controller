import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import socket

  
UDP_IP = '0.0.0.0'
UDP_PORT = '5005'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

class CommandListener(Node):

    def __init__(self):

        super().__init__('UDP_Receiver')

        self.velocity_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

    def command_callback(self, msg):

        #command = msg.data.lower
        # ()

        command = format(msg, '04b')

        twist = Twist()

        if command == 1:

            twist.linear.x = 0.5 # Move forward

        elif command == 2:

            twist.linear.x = -0.5 # Move backward

        elif command == 4:

            twist.angular.z = 1.0 # Turn left

        elif command == 8:

            twist.angular.z = -1.0 # Turn right

        elif command == 0:

            twist.linear.x=0 # Halt

        else:

            self.get_logger().info(f'Unknown command: {command}')

        return

        self.velocity_publisher.publish(twist)

        self.get_logger().info(f'Executing command: {command}')

  

def main(args=None):

    rclpy.init(args=args)
    node = CommandListener()
    data, addr = sock.recvfrom(1024)
    msg = data[0]
    node.command_callback(msg)
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == '__main__':

    main()