// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from uav_interfaces:msg/Obstacle.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__OBSTACLE__BUILDER_HPP_
#define UAV_INTERFACES__MSG__DETAIL__OBSTACLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "uav_interfaces/msg/detail/obstacle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace uav_interfaces
{

namespace msg
{

namespace builder
{

class Init_Obstacle_source_type
{
public:
  explicit Init_Obstacle_source_type(::uav_interfaces::msg::Obstacle & msg)
  : msg_(msg)
  {}
  ::uav_interfaces::msg::Obstacle source_type(::uav_interfaces::msg::Obstacle::_source_type_type arg)
  {
    msg_.source_type = std::move(arg);
    return std::move(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

class Init_Obstacle_confidence
{
public:
  explicit Init_Obstacle_confidence(::uav_interfaces::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_source_type confidence(::uav_interfaces::msg::Obstacle::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_Obstacle_source_type(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

class Init_Obstacle_is_valid
{
public:
  explicit Init_Obstacle_is_valid(::uav_interfaces::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_confidence is_valid(::uav_interfaces::msg::Obstacle::_is_valid_type arg)
  {
    msg_.is_valid = std::move(arg);
    return Init_Obstacle_confidence(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

class Init_Obstacle_is_static
{
public:
  explicit Init_Obstacle_is_static(::uav_interfaces::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_is_valid is_static(::uav_interfaces::msg::Obstacle::_is_static_type arg)
  {
    msg_.is_static = std::move(arg);
    return Init_Obstacle_is_valid(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

class Init_Obstacle_height
{
public:
  explicit Init_Obstacle_height(::uav_interfaces::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_is_static height(::uav_interfaces::msg::Obstacle::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_Obstacle_is_static(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

class Init_Obstacle_radius
{
public:
  explicit Init_Obstacle_radius(::uav_interfaces::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_height radius(::uav_interfaces::msg::Obstacle::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return Init_Obstacle_height(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

class Init_Obstacle_velocity
{
public:
  explicit Init_Obstacle_velocity(::uav_interfaces::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_radius velocity(::uav_interfaces::msg::Obstacle::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_Obstacle_radius(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

class Init_Obstacle_position
{
public:
  explicit Init_Obstacle_position(::uav_interfaces::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_velocity position(::uav_interfaces::msg::Obstacle::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_Obstacle_velocity(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

class Init_Obstacle_id
{
public:
  Init_Obstacle_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Obstacle_position id(::uav_interfaces::msg::Obstacle::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_Obstacle_position(msg_);
  }

private:
  ::uav_interfaces::msg::Obstacle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::uav_interfaces::msg::Obstacle>()
{
  return uav_interfaces::msg::builder::Init_Obstacle_id();
}

}  // namespace uav_interfaces

#endif  // UAV_INTERFACES__MSG__DETAIL__OBSTACLE__BUILDER_HPP_
