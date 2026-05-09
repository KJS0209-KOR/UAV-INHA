// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from uav_interfaces:msg/ObstacleArray.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__OBSTACLE_ARRAY__BUILDER_HPP_
#define UAV_INTERFACES__MSG__DETAIL__OBSTACLE_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "uav_interfaces/msg/detail/obstacle_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace uav_interfaces
{

namespace msg
{

namespace builder
{

class Init_ObstacleArray_obstacles
{
public:
  explicit Init_ObstacleArray_obstacles(::uav_interfaces::msg::ObstacleArray & msg)
  : msg_(msg)
  {}
  ::uav_interfaces::msg::ObstacleArray obstacles(::uav_interfaces::msg::ObstacleArray::_obstacles_type arg)
  {
    msg_.obstacles = std::move(arg);
    return std::move(msg_);
  }

private:
  ::uav_interfaces::msg::ObstacleArray msg_;
};

class Init_ObstacleArray_header
{
public:
  Init_ObstacleArray_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObstacleArray_obstacles header(::uav_interfaces::msg::ObstacleArray::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ObstacleArray_obstacles(msg_);
  }

private:
  ::uav_interfaces::msg::ObstacleArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::uav_interfaces::msg::ObstacleArray>()
{
  return uav_interfaces::msg::builder::Init_ObstacleArray_header();
}

}  // namespace uav_interfaces

#endif  // UAV_INTERFACES__MSG__DETAIL__OBSTACLE_ARRAY__BUILDER_HPP_
