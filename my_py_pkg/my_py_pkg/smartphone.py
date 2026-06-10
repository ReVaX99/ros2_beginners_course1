#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class SmartphoneNode(Node): # Creamos el class --> Object; de clase Nodo
    def __init__(self):
        super().__init__("smartphone") # Le asignamos un nombre al nodo
        self.subscriber_ = self.create_subscription(
            String, "robot_news", self.callback_robot_news, 10) # Usar el mismo message type que el publisher
        self.get_logger().info("Smartphone has been started.")

    def callback_robot_news(self, msg: String):
        self.get_logger().info(msg.data)


def main(args=None):
    rclpy.init(args=args) # Initialize ROS2 communications
    node = SmartphoneNode() # Llamamos al programa main para crear el nodo
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()