// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from uav_interfaces:msg/EgoState.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__EGO_STATE__STRUCT_HPP_
#define UAV_INTERFACES__MSG__DETAIL__EGO_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'velocity'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__uav_interfaces__msg__EgoState __attribute__((deprecated))
#else
# define DEPRECATED__uav_interfaces__msg__EgoState __declspec(deprecated)
#endif

namespace uav_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct EgoState_
{
  using Type = EgoState_<ContainerAllocator>;

  explicit EgoState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    position(_init),
    velocity(_init)
  {
    (void)_init;
  }

  explicit EgoState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    position(_alloc, _init),
    velocity(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _position_type position;
  using _velocity_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _velocity_type velocity;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__position(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__velocity(
    const geometry_msgs::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->velocity = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    uav_interfaces::msg::EgoState_<ContainerAllocator> *;
  using ConstRawPtr =
    const uav_interfaces::msg::EgoState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<uav_interfaces::msg::EgoState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<uav_interfaces::msg::EgoState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      uav_interfaces::msg::EgoState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<uav_interfaces::msg::EgoState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      uav_interfaces::msg::EgoState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<uav_interfaces::msg::EgoState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<uav_interfaces::msg::EgoState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<uav_interfaces::msg::EgoState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__uav_interfaces__msg__EgoState
    std::shared_ptr<uav_interfaces::msg::EgoState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__uav_interfaces__msg__EgoState
    std::shared_ptr<uav_interfaces::msg::EgoState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EgoState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    return true;
  }
  bool operator!=(const EgoState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EgoState_

// alias to use template instance with default allocator
using EgoState =
  uav_interfaces::msg::EgoState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace uav_interfaces

#endif  // UAV_INTERFACES__MSG__DETAIL__EGO_STATE__STRUCT_HPP_
