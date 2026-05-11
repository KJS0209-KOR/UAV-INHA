// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from uav_interfaces:msg/ObstacleArray.idl
// generated code does not contain a copyright notice

#ifndef UAV_INTERFACES__MSG__DETAIL__OBSTACLE_ARRAY__STRUCT_H_
#define UAV_INTERFACES__MSG__DETAIL__OBSTACLE_ARRAY__STRUCT_H_

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
// Member 'obstacles'
#include "uav_interfaces/msg/detail/obstacle__struct.h"

/// Struct defined in msg/ObstacleArray in the package uav_interfaces.
typedef struct uav_interfaces__msg__ObstacleArray
{
  std_msgs__msg__Header header;
  uav_interfaces__msg__Obstacle__Sequence obstacles;
} uav_interfaces__msg__ObstacleArray;

// Struct for a sequence of uav_interfaces__msg__ObstacleArray.
typedef struct uav_interfaces__msg__ObstacleArray__Sequence
{
  uav_interfaces__msg__ObstacleArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} uav_interfaces__msg__ObstacleArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // UAV_INTERFACES__MSG__DETAIL__OBSTACLE_ARRAY__STRUCT_H_
