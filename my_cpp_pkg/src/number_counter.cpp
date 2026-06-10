#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"
#include "example_interfaces/srv/set_bool.hpp"

using namespace std::chrono_literals;
using namespace std::placeholders;

class NumberCounter : public rclcpp::Node
{
public:
    NumberCounter() : Node("number_counter")
    {
        publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number_count", 10);
        subscriber_ = this->create_subscription<example_interfaces::msg::Int64>(
            "number", 10,
            std::bind(&NumberCounter::callbackNumberCounter, this, _1));
        server_ = this->create_service<example_interfaces::srv::SetBool>(
            "reset_counter", 
            std::bind(&NumberCounter::callbackResetCounter, this, _1));
        RCLCPP_INFO(this->get_logger(), "Number Counter has been started.");
    }

private:
    void callbackResetCounter(const example_interfaces::srv::SetBool::Request::SharedPtr request)
    {
        if (request->data == true){
            counter_ = 0;
            RCLCPP_INFO(this->get_logger(), "Number Counter has been reset to 0.");
        } else {
            RCLCPP_INFO(this->get_logger(), "Number Counter continues adding up.");
        }
        
    }


    void callbackNumberCounter(const example_interfaces::msg::Int64::SharedPtr msg)
    {
        auto new_msg = example_interfaces::msg::Int64();
        counter_ = msg->data + counter_; 
        new_msg.data = counter_;
        publisher_->publish(new_msg);
    }

    rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscriber_;
    rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
    int64_t counter_ = 0;
    rclcpp::Service<example_interfaces::srv::SetBool>::SharedPtr server_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberCounter>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}



