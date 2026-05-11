// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from uav_interfaces:msg/EgoState.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__EGO_STATE__STRUCT_H_
#define UAV_INTERFACES__MSG__DETAIL__EGO_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'velocity'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in msg/EgoState in the package uav_interfaces.
typedef struct uav_interfaces__msg__EgoState
{
  std_msgs__msg__Header header;
  geometry_msgs__msg__Point position;
  geometry_msgs__msg__Vector3 velocity;
} uav_interfaces__msg__EgoState;

// Struct for a sequence of uav_interfaces__msg__EgoState.
typedef struct uav_interfaces__msg__EgoState__Sequence
{
  uav_interfaces__msg__EgoState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} uav_interfaces__msg__EgoState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UAV_INTERFACES__MSG__DETAIL__EGO_STATE__STRUCT_H_
