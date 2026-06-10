#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedPanelState
from my_robot_interfaces.srv import SetLed


class LedPanelPublisherNode(Node):
    def __init__(self):
        super().__init__("led_panel_publisher") # Inicias la class
        self.ld_status_pub_ = self.create_publisher(LedPanelState, "led_panel_state", 10) # Defines el publisher
        self.timer_ = self.create_timer(1.0, self.publish_lp_status) # Creas un timer para publish con el callback del method que publica
        self.server_ = self.create_service(SetLed, "set_led", self.callback_set_led)
        self.msg_ = LedPanelState()
        self.declare_parameter("leds_state", [0, 0, 0])
        self.msg_.leds = self.get_parameter("leds_state").value
        self.get_logger().info("Led Panel Status publisher has been started") # Getlogger para informar de que el nodo se ha iniciado OK


    def callback_set_led(self, request: SetLed.Request, response: SetLed.Response):
        if request.empty_battery == True: 
            self.msg_.leds[2] = 1
            response.led_on_success = True
            self.get_logger().info("Low battery received. Turning LED 3 ON")
            self.ld_status_pub_.publish(self.msg_)

        else: 
            self.msg_.leds[2] = 0
            response.led_on_success = False
            self.get_logger().info("Full battery received. Turning LED 3 OFF")
            self.ld_status_pub_.publish(self.msg_)

        return response


    def publish_lp_status(self): # Le tengo que pasar self para acceder a ld_status_pub
             
        # Publico el mensaje que recibo
        self.ld_status_pub_.publish(self.msg_)


def main(args=None):
    rclpy.init(args=args)
    node = LedPanelPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()