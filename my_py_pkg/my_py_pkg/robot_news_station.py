#!/usr/bin/env python3
import rclpy #ros2 library for pyhton
from rclpy.node import Node
from example_interfaces.msg import String


class RobotNewStationNode(Node):

    def __init__(self):
        super().__init__("robot_news_station")
        self.declare_parameter("robot_name", "C3PO")
        self.robot_name_ = self.get_parameter("robot_name").value
        self.publisher_=self.create_publisher(String, "robot_news", 10)
        self.timer_ = self.create_timer(0.5, self.publish_news)
        self.get_logger().info("Robot News Station has been started.")

    def publish_news(self):
        msg = String()
        msg.data = "Hi, this is " + self.robot_name_+ " from the robot news station."
        self.publisher_.publish(msg)



def main(args=None):
    rclpy.init(args=args) # Initialize ros2 communication
    node = RobotNewStationNode() # We codereate the node
    rclpy.spin(node) # Este spin es para mantener el nodo vivo. Sin ctrl + C no se deja de ejecutar el nodo
    rclpy.shutdown() # Finalise communication

if __name__ == "__main__": # Esto llama a la funcion main por defecto
    main()