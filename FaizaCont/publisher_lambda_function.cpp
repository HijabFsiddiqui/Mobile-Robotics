// Copyright 2016 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#include <iostream>
#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/char.hpp"

using namespace std::chrono_literals;

/* This example creates a subclass of Node and uses a fancy C++11 lambda
 * function to shorten the callback syntax, at the expense of making the
 * code somewhat more difficult to understand at first glance. */

class MinimalPublisher : public rclcpp::Node
{
public:
  MinimalPublisher()
  : Node("minimal_publisher")
  {
    publisher_ = this->create_publisher<std_msgs::msg::Char>("topic", 10);
    
  }
    
    void publish_char(char c) {
    	auto message = std_msgs::msg::Char();
    	message.data = static_cast<uint8_t>(c);
    	RCLCPP_INFO(this->get_logger(), "Publishing: '%c'", c);
    	publisher_->publish(message);
    }

private:
  rclcpp::Publisher<std_msgs::msg::Char>::SharedPtr publisher_;
};

int main(int argc, char * argv[])
{
  
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MinimalPublisher>();

  std::string line;
  while (rclcpp::ok()) {
    std::cout << "Enter a character: " << std::flush;
    if (!std::getline(std::cin, line)) {
      break;  // Ctrl+D exits
    }
    if (line.empty()) {
      continue;
    }
    if (line.size() > 1) {
      RCLCPP_WARN(node->get_logger(), "Only the first character '%c' will be sent", line[0]);
    }
    node->publish_char(line[0]);
  }

  rclcpp::shutdown();
  return 0;
}
