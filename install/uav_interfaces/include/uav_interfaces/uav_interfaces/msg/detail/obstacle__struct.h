// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from uav_interfaces:msg/Obstacle.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__OBSTACLE__STRUCT_H_
#define UAV_INTERFACES__MSG__DETAIL__OBSTACLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'id'
// Member 'source_type'
#include "rosidl_runtime_c/string.h"
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'velocity'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in msg/Obstacle in the package uav_interfaces.
typedef struct uav_interfaces__msg__Obstacle
{
  rosidl_runtime_c__String id;
  geometry_msgs__msg__Point position;
  geometry_msgs__msg__Vector3 velocity;
  float radius;
  float height;
  bool is_static;
  bool is_valid;
  float confidence;
  rosidl_runtime_c__String source_type;
} uav_interfaces__msg__Obstacle;

// Struct for a sequence of uav_interfaces__msg__Obstacle.
typedef struct uav_interfaces__msg__Obstacle__Sequence
{
  uav_interfaces__msg__Obstacle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} uav_interfaces__msg__Obstacle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UAV_INTERFACES__MSG__DETAIL__OBSTACLE__STRUCT_H_
