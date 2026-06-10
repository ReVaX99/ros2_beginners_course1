#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleSpeedTest(Node):
    def __init__(self):
        super().__init__("turtle_speed_test")
        self.linear_x_ = 5.0
        self.speed_publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer_ = self.create_timer(1.0, self.publish_speed)

    def publish_speed(self):
        speed = Twist()
        speed.linear.x = self.linear_x_
        self.speed_publisher_.publish(speed)
        pass



def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpeedTest()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()