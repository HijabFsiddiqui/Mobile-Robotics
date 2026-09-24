#include <chrono>
#include <cmath>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

using namespace std::chrono_literals;

class CosineMover : public rclcpp::Node
{
public:
  CosineMover()
  : Node("cosine_mover")
  {
    A_ = this->declare_parameter("amplitude", 1.0);
    lambda_ = this->declare_parameter("wavelength", 4.0);
    c_ = this->declare_parameter("forward_speed", 1.0);
    duration_ = this->declare_parameter("duration", 9.0);
    w_ = 2.0 * M_PI * c_ / lambda_;

    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
    start_ = this->now();
    timer_ = this->create_wall_timer(20ms, [this]() { step(); });
  }

private:
  void step()
  {
    double t = (this->now() - start_).seconds();
    geometry_msgs::msg::Twist cmd;

    if (t >= duration_) {
      publisher_->publish(cmd);
      RCLCPP_INFO(this->get_logger(), "Done");
      timer_->cancel();
      return;
    }

    double vx = c_;
    double vy = -A_ * w_ * std::sin(w_ * t);
    double ay = -A_ * w_ * w_ * std::cos(w_ * t);

    cmd.linear.x = std::hypot(vx, vy);
    cmd.angular.z = (vx * ay) / (vx * vx + vy * vy);
    publisher_->publish(cmd);
  }

  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Time start_;
  double A_, lambda_, c_, w_, duration_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CosineMover>());
  rclcpp::shutdown();
  return 0;
}
