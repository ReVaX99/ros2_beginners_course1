#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from my_robot_interfaces.msg import TurtleAlive, TurtleAliveArray
import random
from functools import partial


class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner_node")
        self.turtle_spawner_client_ = self.create_client(Spawn, "spawn")
        self.turtles_array_history_ = []
        self.declare_parameter("spawn_period", 2.0)
        self.timer_period_ = self.get_parameter("spawn_period").value
        self.spawn_timer_ = self.create_timer(self.timer_period_, self.callback_turtle_spawner)
        self.alive_turtles_publisher_ = self.create_publisher(TurtleAlive, "alive_turtles", 10)
        self.alive_turtles_array_publisher_ = self.create_publisher(TurtleAliveArray, "alive_turtles_array", 10)      
        self.catch_turtle_server_ = self.create_service(Kill, "kill_turtle", self.callback_kill_turtle)
        self.get_logger().info("Turtle Spawner Node has been initialized.")


    # Continue defining the functions below the next day. How to eliminate turtles when you get their name
    def callback_kill_turtle(self, request: Kill.Request):
        for i in self.turtles_array_history_:
            if self.turtles_array_history_[i, 3] == request.name:
                pass


    def callback_turtle_spawner(self):
        x = random.uniform(0, 11)
        y = random.uniform(0, 11)
        theta = random.uniform(0, 360)
        self.turtle_spawn_request(x, y, theta)
        
    
    def turtle_spawn_request(self, x, y, theta):
        while not self.turtle_spawner_client_.wait_for_service(2.0):
            self.get_logger().info("Waiting to spawn a new turtle")

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta

        future = self.turtle_spawner_client_.call_async(request)
        future.add_done_callback(partial(self.callback_new_turtle_spawned, x=x, y=y, theta=theta))


    def callback_new_turtle_spawned(self, future, x, y, theta):
        msg = TurtleAlive()
        turtles_array = TurtleAliveArray()
        msg.x = x
        msg.y = y
        msg.theta = theta
        response = future.result()
        msg.name = response.name
        self.turtles_array_history_.append(msg)
        turtles_array.turtles = self.turtles_array_history_
        self.alive_turtles_publisher_.publish(msg)
        self.alive_turtles_array_publisher_.publish(turtles_array)
        self.get_logger().info(str(response.name) + " has spawned.")


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()