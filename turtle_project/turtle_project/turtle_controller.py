#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Kill
from geometry_msgs.msg import Twist
from my_robot_interfaces.msg import TurtleAliveArray

class TurtleControllerNode(Node):
    def __init__(self):
        super().__init__("turtle_controller")
        self.target_x : float = 5.5445
        self.target_y : float = 5.5445
        self.target_name : str = None
        self.caught_turtles = set()
        self.pose_subscriber_ = self.create_subscription(Pose, "/turtle1/pose", self.callback_pose, 10)
        self.pose_ : Pose = None
        self.cmd_vel_publisher_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.min_dist_subscriber_ = self.create_subscription(TurtleAliveArray, "alive_turtles_array",self.callback_min_distance, 10)
        self.kill_turtle_client_ = self.create_client(Kill, "kill")
        self.control_loop_timer_ = self.create_timer(0.01, self.control_loop)

    def callback_pose(self, pose: Pose):
        self.pose_ = pose
    
    def callback_min_distance(self, msg: TurtleAliveArray):
        if self.target_x == -1.0:
            # Not initialized
            pass

        min_distance = 100.0   

        for turtle in msg.turtles:
            #self.get_logger().info(f"{turtle.x}, {turtle.y}") #Used for debugging
            if turtle.name in self.caught_turtles: continue
            dist_x = turtle.x - self.pose_.x
            dist_y = turtle.y - self.pose_.y
            distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
            if distance < min_distance:
                min_distance = distance
                min_pose_x = turtle.x
                min_pose_y = turtle.y
                min_pose_name = turtle.name
        

        self.target_x = min_pose_x
        self.target_y = min_pose_y
        self.target_name = min_pose_name
        #self.get_logger().info(f"Goal targets: X={self.target_x}, Y={self.target_y}, Turtle name={self.target_name}")


    def control_loop(self):
        if self.pose_ == None:
            return
        
        dist_x = self.target_x - self.pose_.x
        dist_y = self.target_y - self.pose_.y
        distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)

        cmd = Twist()

        if distance > 0.5:
            # position
            cmd.linear.x = 2*distance # Este es mi P controller para la distance

            # orientation
            goal_theta = math.atan2(dist_y, dist_x)
            diff = goal_theta - self.pose_.theta
            if diff > math.pi:
                diff -= 2*math.pi
            elif diff < -math.pi:
                diff += 2*math.pi
            
            cmd.angular.z = 6*diff # Este es mi P controller para el angulo

        else:
            # target reached
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            
            if self.target_name == None: pass
            else: 
                self.caught_turtles.add(self.target_name)
                self.call_kill_turtle()
                self.target_name = None # Es necesario inicializar otra vez el nombre de la tortuga a la que matar. Sino, da error todo el rato hasta que se le asigna un nuevo valor por la exec freq del control loop
            
            #self.get_clock().sleep_for(rclpy.duration.Duration(seconds=0.5))
            

        self.cmd_vel_publisher_.publish(cmd)


    def call_kill_turtle(self):
        while not self.kill_turtle_client_.wait_for_service(1.0):
           self.get_logger().warn("Waiting for Kill Service...")
    
        request = Kill.Request()
        request.name = self.target_name
        self.kill_turtle_client_.call_async(request)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()