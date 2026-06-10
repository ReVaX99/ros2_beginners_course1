#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from example_interfaces.msg import Int64 # Type for the topic that we use


class NumberPublisher(Node): 
    def __init__(self):
        super().__init__("number_publisher")
        self.declare_parameter("number", 2) # Parameter declared
        self.declare_parameter("timer_period", 1.0)
        self.number_publisher_ = self.create_publisher(Int64, "number", 10) # Create the publisher
        self.number_ = self.get_parameter("number").value # Get value for the parameter
        self.timer_period_ = self.get_parameter("timer_period").value
        #self.counter_ = 0 # Create a counter atribute
        self.add_post_set_parameters_callback(self.parameters_callback_)
        self.number_timer_ = self.create_timer(self.timer_period_, self.publish_number) # Create the timer at which a method is executed
        self.get_logger().info("Number Publisher has been started.") # Get logger once we initialize the node

    def publish_number(self): # We define the method
        msg = Int64() # We define a variable of Int64 class type
        # self.counter_ = self.counter_ + 2 # We update the counter at each cycle
        msg.data = self.number_# We assign the value of the counter to number.data to be able to publish it
        self.number_publisher_.publish(msg)
        #self.publisher_.publish(msg)

    def parameters_callback_(self, params: list[Parameter]):
        for param in params:
            if param.name == "number":
                self.number_ = param.value

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()