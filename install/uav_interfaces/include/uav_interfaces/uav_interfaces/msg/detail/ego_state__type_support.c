// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from uav_interfaces:msg/EgoState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "uav_interfaces/msg/detail/ego_state__rosidl_typesupport_introspection_c.h"
#include "uav_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "uav_interfaces/msg/detail/ego_state__functions.h"
#include "uav_interfaces/msg/detail/ego_state__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `position`
#include "geometry_msgs/msg/point.h"
// Member `position`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"
// Member `velocity`
#include "geometry_msgs/msg/vector3.h"
// Member `velocity`
#include "geometry_msgs/msg/detail/vector3__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  uav_interfaces__msg__EgoState__init(message_memory);
}

void uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_fini_function(void * message_memory)
{
  uav_interfaces__msg__EgoState__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_interfaces__msg__EgoState, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_interfaces__msg__EgoState, position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(uav_interfaces__msg__EgoState, velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_members = {
  "uav_interfaces__msg",  // message namespace
  "EgoState",  // message name
  3,  // number of fields
  sizeof(uav_interfaces__msg__EgoState),
  uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_member_array,  // message members
  uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_init_function,  // function to initialize message memory (memory has to be allocated)
  uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_type_support_handle = {
  0,
  &uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_uav_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, uav_interfaces, msg, EgoState)() {
  uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Vector3)();
  if (!uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_type_support_handle.typesupport_identifier) {
    uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &uav_interfaces__msg__EgoState__rosidl_typesupport_introspection_c__EgoState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
