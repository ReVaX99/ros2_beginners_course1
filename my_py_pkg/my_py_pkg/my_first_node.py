#!/usr/bin/env python3
import rclpy #ros2 library for pyhton
from rclpy.node import Node


class MyNode(Node):

    def __init__(self):
        super().__init__("py_test")
        self.counter_ = 0
        self.get_logger().info("Hello world")
        self.create_timer(1.0, self.timer_callback)
    
    def timer_callback(self):
        self.get_logger().info("Hello " + str(self.counter_))
        self.counter_ += 1


def main(args=None):
    rclpy.init(args=args) # Initialize ros2 communication
    node = MyNode() # We codereate the node
    rclpy.spin(node) # Este spin es para mantener el nodo vivo. Sin ctrl + C no se deja de ejecutar el nodo
    rclpy.shutdown() # Finalise communication

if __name__ == "__main__": # Esto llama a la funcion main por defecto
    main()



