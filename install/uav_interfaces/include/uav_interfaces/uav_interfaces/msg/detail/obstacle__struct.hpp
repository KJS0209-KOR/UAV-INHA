// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from uav_interfaces:msg/Obstacle.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__OBSTACLE__STRUCT_HPP_
#define UAV_INTERFACES__MSG__DETAIL__OBSTACLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'velocity'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__uav_interfaces__msg__Obstacle __attribute__((deprecated))
#else
# define DEPRECATED__uav_interfaces__msg__Obstacle __declspec(deprecated)
#endif

namespace uav_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Obstacle_
{
  using Type = Obstacle_<ContainerAllocator>;

  explicit Obstacle_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : position(_init),
    velocity(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = "";
      this->radius = 0.0f;
      this->height = 0.0f;
      this->is_static = false;
      this->is_valid = false;
      this->confidence = 0.0f;
      this->source_type = "";
    }
  }

  explicit Obstacle_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : id(_alloc),
    position(_alloc, _init),
    velocity(_alloc, _init),
    source_type(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = "";
      this->radius = 0.0f;
      this->height = 0.0f;
      this->is_static = false;
      this->is_valid = false;
      this->confidence = 0.0f;
      this->source_type = "";
    }
  }

  // field types and members
  using _id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _id_type id;
  using _position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _position_type position;
  using _velocity_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _velocity_type velocity;
  using _radius_type =
    float;
  _radius_type radius;
  using _height_type =
    float;
  _height_type height;
  using _is_static_type =
    bool;
  _is_static_type is_static;
  using _is_valid_type =
    bool;
  _is_valid_type is_valid;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _source_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _source_type_type source_type;

  // setters for named parameter idiom
  Type & set__id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->id = _arg;
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
  Type & set__radius(
    const float & _arg)
  {
    this->radius = _arg;
    return *this;
  }
  Type & set__height(
    const float & _arg)
  {
    this->height = _arg;
    return *this;
  }
  Type & set__is_static(
    const bool & _arg)
  {
    this->is_static = _arg;
    return *this;
  }
  Type & set__is_valid(
    const bool & _arg)
  {
    this->is_valid = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__source_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->source_type = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    uav_interfaces::msg::Obstacle_<ContainerAllocator> *;
  using ConstRawPtr =
    const uav_interfaces::msg::Obstacle_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<uav_interfaces::msg::Obstacle_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<uav_interfaces::msg::Obstacle_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      uav_interfaces::msg::Obstacle_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<uav_interfaces::msg::Obstacle_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      uav_interfaces::msg::Obstacle_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<uav_interfaces::msg::Obstacle_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<uav_interfaces::msg::Obstacle_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<uav_interfaces::msg::Obstacle_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__uav_interfaces__msg__Obstacle
    std::shared_ptr<uav_interfaces::msg::Obstacle_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__uav_interfaces__msg__Obstacle
    std::shared_ptr<uav_interfaces::msg::Obstacle_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Obstacle_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->radius != other.radius) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    if (this->is_static != other.is_static) {
      return false;
    }
    if (this->is_valid != other.is_valid) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->source_type != other.source_type) {
      return false;
    }
    return true;
  }
  bool operator!=(const Obstacle_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Obstacle_

// alias to use template instance with default allocator
using Obstacle =
  uav_interfaces::msg::Obstacle_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace uav_interfaces

#endif  // UAV_INTERFACES__MSG__DETAIL__OBSTACLE__STRUCT_HPP_
