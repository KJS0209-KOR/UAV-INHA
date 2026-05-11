// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from uav_interfaces:msg/ObstacleArray.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "uav_interfaces/msg/detail/obstacle_array__rosidl_typesupport_introspection_c.h"
#include "uav_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "uav_interfaces/msg/detail/obstacle_array__functions.h"
#include "uav_interfaces/msg/detail/obstacle_array__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `obstacles`
#include "uav_interfaces/msg/obstacle.h"
// Member `obstacles`
#include "uav_interfaces/msg/detail/obstacle__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  uav_interfaces__msg__ObstacleArray__init(message_memory);
}

void uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_fini_function(void * message_memory)
{
  uav_interfaces__msg__ObstacleArray__fini(message_memory);
}

size_t uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__size_function__ObstacleArray__obstacles(
  const void * untyped_member)
{
  const uav_interfaces__msg__Obstacle__Sequence * member =
    (const uav_interfaces__msg__Obstacle__Sequence *)(untyped_member);
  return member->size;
}

const void * uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__get_const_function__ObstacleArray__obstacles(
  const void * untyped_member, size_t index)
{
  const uav_interfaces__msg__Obstacle__Sequence * member =
    (const uav_interfaces__msg__Obstacle__Sequence *)(untyped_member);
  return &member->data[index];
}

void * uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__get_function__ObstacleArray__obstacles(
  void * untyped_member, size_t index)
{
  uav_interfaces__msg__Obstacle__Sequence * member =
    (uav_interfaces__msg__Obstacle__Sequence *)(untyped_member);
  return &member->data[index];
}

void uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__fetch_function__ObstacleArray__obstacles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uav_interfaces__msg__Obstacle * item =
    ((const uav_interfaces__msg__Obstacle *)
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__get_const_function__ObstacleArray__obstacles(untyped_member, index));
  uav_interfaces__msg__Obstacle * value =
    (uav_interfaces__msg__Obstacle *)(untyped_value);
  *value = *item;
}

void uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__assign_function__ObstacleArray__obstacles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uav_interfaces__msg__Obstacle * item =
    ((uav_interfaces__msg__Obstacle *)
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__get_function__ObstacleArray__obstacles(untyped_member, index));
  const uav_interfaces__msg__Obstacle * value =
    (const uav_interfaces__msg__Obstacle *)(untyped_value);
  *item = *value;
}

bool uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__resize_function__ObstacleArray__obstacles(
  void * untyped_member, size_t size)
{
  uav_interfaces__msg__Obstacle__Sequence * member =
    (uav_interfaces__msg__Obstacle__Sequence *)(untyped_member);
  uav_interfaces__msg__Obstacle__Sequence__fini(member);
  return uav_interfaces__msg__Obstacle__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_interfaces__msg__ObstacleArray, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "obstacles",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_interfaces__msg__ObstacleArray, obstacles),  // bytes offset in struct
    NULL,  // default value
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__size_function__ObstacleArray__obstacles,  // size() function pointer
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__get_const_function__ObstacleArray__obstacles,  // get_const(index) function pointer
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__get_function__ObstacleArray__obstacles,  // get(index) function pointer
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__fetch_function__ObstacleArray__obstacles,  // fetch(index, &value) function pointer
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__assign_function__ObstacleArray__obstacles,  // assign(index, value) function pointer
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__resize_function__ObstacleArray__obstacles  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_members = {
  "uav_interfaces__msg",  // message namespace
  "ObstacleArray",  // message name
  2,  // number of fields
  sizeof(uav_interfaces__msg__ObstacleArray),
  uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_member_array,  // message members
  uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_init_function,  // function to initialize message memory (memory has to be allocated)
  uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_type_support_handle = {
  0,
  &uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_uav_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, uav_interfaces, msg, ObstacleArray)() {
  uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, uav_interfaces, msg, Obstacle)();
  if (!uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_type_support_handle.typesupport_identifier) {
    uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &uav_interfaces__msg__ObstacleArray__rosidl_typesupport_introspection_c__ObstacleArray_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
