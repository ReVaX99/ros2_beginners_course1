#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed


class BatteryClientNode(Node):
    def __init__(self):
        super().__init__("battery_client_node")
        self.client_ = self.create_client(SetLed, "set_led")
        self.led_state_ = True
        self.timer_period_ = 6.0
        self.timer_ = self.create_timer(self.timer_period_, self.timer_callback)
        self.get_logger().info("Battery Client Node has been started successfully")
        
    def timer_callback(self):
        
        self.timer_.cancel()

        if self.timer_period_ == 6.0:
            self.timer_period_ = 4.0
            self.get_logger().info("Sending request: Empty battery (True)")
            self.led_state_ = True
            self.call_set_led(self.led_state_)

        else: 
            self.timer_period_ = 6.0
            self.get_logger().info("Sending request: Full battery (False)")
            self.led_state_ = False
            self.call_set_led(self.led_state_)
            
        self.timer_ = self.create_timer(self.timer_period_, self.timer_callback)


    def call_set_led(self, battery_state):

        while not self.client_.wait_for_service(1.0): # Here we wait for the service to be up
            self.get_logger().warn("Waiting for Set Led server...")

        # Here, the request is created
        request = SetLed.Request()
        request.empty_battery = battery_state # Battery state can be true (empty battery) or false (full battery)

        # Request is sent asynchronouslyS
        future = self.client_.call_async(request) # We send the request with this line to the server, and we save it as a future
        future.add_done_callback(self.callback_call_battery_state) # This is to spin while we wait the server to reply. A callback will be called once an answer is received.

    def callback_call_battery_state(self, future):
        response = future.result()
        self.get_logger().info("Got response: " + str(response.led_on_success))


def main(args=None):
    rclpy.init(args=args)
    node = BatteryClientNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()