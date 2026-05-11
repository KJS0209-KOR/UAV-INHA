// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from uav_interfaces:msg/EgoState.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__EGO_STATE__TRAITS_HPP_
#define UAV_INTERFACES__MSG__DETAIL__EGO_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "uav_interfaces/msg/detail/ego_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'position'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'velocity'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"

namespace uav_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const EgoState & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: position
  {
    out << "position: ";
    to_flow_style_yaml(msg.position, out);
    out << ", ";
  }

  // member: velocity
  {
    out << "velocity: ";
    to_flow_style_yaml(msg.velocity, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const EgoState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position:\n";
    to_block_style_yaml(msg.position, out, indentation + 2);
  }

  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocity:\n";
    to_block_style_yaml(msg.velocity, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const EgoState & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace uav_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use uav_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const uav_interfaces::msg::EgoState & msg,
  std::ostream & out, size_t indentation = 0)
{
  uav_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use uav_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const uav_interfaces::msg::EgoState & msg)
{
  return uav_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<uav_interfaces::msg::EgoState>()
{
  return "uav_interfaces::msg::EgoState";
}

template<>
inline const char * name<uav_interfaces::msg::EgoState>()
{
  return "uav_interfaces/msg/EgoState";
}

template<>
struct has_fixed_size<uav_interfaces::msg::EgoState>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value && has_fixed_size<geometry_msgs::msg::Vector3>::value && has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<uav_interfaces::msg::EgoState>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value && has_bounded_size<geometry_msgs::msg::Vector3>::value && has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<uav_interfaces::msg::EgoState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UAV_INTERFACES__MSG__DETAIL__EGO_STATE__TRAITS_HPP_
