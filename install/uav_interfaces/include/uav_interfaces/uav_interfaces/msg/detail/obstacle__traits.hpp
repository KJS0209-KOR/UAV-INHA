// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from uav_interfaces:msg/Obstacle.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__OBSTACLE__TRAITS_HPP_
#define UAV_INTERFACES__MSG__DETAIL__OBSTACLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "uav_interfaces/msg/detail/obstacle__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'position'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'velocity'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"

namespace uav_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Obstacle & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
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
    out << ", ";
  }

  // member: radius
  {
    out << "radius: ";
    rosidl_generator_traits::value_to_yaml(msg.radius, out);
    out << ", ";
  }

  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << ", ";
  }

  // member: is_static
  {
    out << "is_static: ";
    rosidl_generator_traits::value_to_yaml(msg.is_static, out);
    out << ", ";
  }

  // member: is_valid
  {
    out << "is_valid: ";
    rosidl_generator_traits::value_to_yaml(msg.is_valid, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: source_type
  {
    out << "source_type: ";
    rosidl_generator_traits::value_to_yaml(msg.source_type, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Obstacle & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
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

  // member: radius
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "radius: ";
    rosidl_generator_traits::value_to_yaml(msg.radius, out);
    out << "\n";
  }

  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }

  // member: is_static
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_static: ";
    rosidl_generator_traits::value_to_yaml(msg.is_static, out);
    out << "\n";
  }

  // member: is_valid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_valid: ";
    rosidl_generator_traits::value_to_yaml(msg.is_valid, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: source_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "source_type: ";
    rosidl_generator_traits::value_to_yaml(msg.source_type, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Obstacle & msg, bool use_flow_style = false)
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
  const uav_interfaces::msg::Obstacle & msg,
  std::ostream & out, size_t indentation = 0)
{
  uav_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use uav_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const uav_interfaces::msg::Obstacle & msg)
{
  return uav_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<uav_interfaces::msg::Obstacle>()
{
  return "uav_interfaces::msg::Obstacle";
}

template<>
inline const char * name<uav_interfaces::msg::Obstacle>()
{
  return "uav_interfaces/msg/Obstacle";
}

template<>
struct has_fixed_size<uav_interfaces::msg::Obstacle>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<uav_interfaces::msg::Obstacle>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<uav_interfaces::msg::Obstacle>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // UAV_INTERFACES__MSG__DETAIL__OBSTACLE__TRAITS_HPP_
