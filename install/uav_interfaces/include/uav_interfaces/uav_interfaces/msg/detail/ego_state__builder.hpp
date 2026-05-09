// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from uav_interfaces:msg/EgoState.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__EGO_STATE__BUILDER_HPP_
#define UAV_INTERFACES__MSG__DETAIL__EGO_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "uav_interfaces/msg/detail/ego_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace uav_interfaces
{

namespace msg
{

namespace builder
{

class Init_EgoState_velocity
{
public:
  explicit Init_EgoState_velocity(::uav_interfaces::msg::EgoState & msg)
  : msg_(msg)
  {}
  ::uav_interfaces::msg::EgoState velocity(::uav_interfaces::msg::EgoState::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::uav_interfaces::msg::EgoState msg_;
};

class Init_EgoState_position
{
public:
  explicit Init_EgoState_position(::uav_interfaces::msg::EgoState & msg)
  : msg_(msg)
  {}
  Init_EgoState_velocity position(::uav_interfaces::msg::EgoState::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_EgoState_velocity(msg_);
  }

private:
  ::uav_interfaces::msg::EgoState msg_;
};

class Init_EgoState_header
{
public:
  Init_EgoState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_EgoState_position header(::uav_interfaces::msg::EgoState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_EgoState_position(msg_);
  }

private:
  ::uav_interfaces::msg::EgoState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::uav_interfaces::msg::EgoState>()
{
  return uav_interfaces::msg::builder::Init_EgoState_header();
}

}  // namespace uav_interfaces

#endif  // UAV_INTERFACES__MSG__DETAIL__EGO_STATE__BUILDER_HPP_
