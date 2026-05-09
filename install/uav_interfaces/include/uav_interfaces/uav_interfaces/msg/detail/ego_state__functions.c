// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from uav_interfaces:msg/EgoState.idl
// generated code does not contain a copyright notice
#include "uav_interfaces/msg/detail/ego_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `position`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `velocity`
#include "geometry_msgs/msg/detail/vector3__functions.h"

bool
uav_interfaces__msg__EgoState__init(uav_interfaces__msg__EgoState * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    uav_interfaces__msg__EgoState__fini(msg);
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__init(&msg->position)) {
    uav_interfaces__msg__EgoState__fini(msg);
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Vector3__init(&msg->velocity)) {
    uav_interfaces__msg__EgoState__fini(msg);
    return false;
  }
  return true;
}

void
uav_interfaces__msg__EgoState__fini(uav_interfaces__msg__EgoState * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // position
  geometry_msgs__msg__Point__fini(&msg->position);
  // velocity
  geometry_msgs__msg__Vector3__fini(&msg->velocity);
}

bool
uav_interfaces__msg__EgoState__are_equal(const uav_interfaces__msg__EgoState * lhs, const uav_interfaces__msg__EgoState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->position), &(rhs->position)))
  {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Vector3__are_equal(
      &(lhs->velocity), &(rhs->velocity)))
  {
    return false;
  }
  return true;
}

bool
uav_interfaces__msg__EgoState__copy(
  const uav_interfaces__msg__EgoState * input,
  uav_interfaces__msg__EgoState * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__copy(
      &(input->position), &(output->position)))
  {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Vector3__copy(
      &(input->velocity), &(output->velocity)))
  {
    return false;
  }
  return true;
}

uav_interfaces__msg__EgoState *
uav_interfaces__msg__EgoState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_interfaces__msg__EgoState * msg = (uav_interfaces__msg__EgoState *)allocator.allocate(sizeof(uav_interfaces__msg__EgoState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(uav_interfaces__msg__EgoState));
  bool success = uav_interfaces__msg__EgoState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
uav_interfaces__msg__EgoState__destroy(uav_interfaces__msg__EgoState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    uav_interfaces__msg__EgoState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
uav_interfaces__msg__EgoState__Sequence__init(uav_interfaces__msg__EgoState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_interfaces__msg__EgoState * data = NULL;

  if (size) {
    data = (uav_interfaces__msg__EgoState *)allocator.zero_allocate(size, sizeof(uav_interfaces__msg__EgoState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = uav_interfaces__msg__EgoState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        uav_interfaces__msg__EgoState__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
uav_interfaces__msg__EgoState__Sequence__fini(uav_interfaces__msg__EgoState__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      uav_interfaces__msg__EgoState__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

uav_interfaces__msg__EgoState__Sequence *
uav_interfaces__msg__EgoState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  uav_interfaces__msg__EgoState__Sequence * array = (uav_interfaces__msg__EgoState__Sequence *)allocator.allocate(sizeof(uav_interfaces__msg__EgoState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = uav_interfaces__msg__EgoState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
uav_interfaces__msg__EgoState__Sequence__destroy(uav_interfaces__msg__EgoState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    uav_interfaces__msg__EgoState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
uav_interfaces__msg__EgoState__Sequence__are_equal(const uav_interfaces__msg__EgoState__Sequence * lhs, const uav_interfaces__msg__EgoState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!uav_interfaces__msg__EgoState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
uav_interfaces__msg__EgoState__Sequence__copy(
  const uav_interfaces__msg__EgoState__Sequence * input,
  uav_interfaces__msg__EgoState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(uav_interfaces__msg__EgoState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    uav_interfaces__msg__EgoState * data =
      (uav_interfaces__msg__EgoState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!uav_interfaces__msg__EgoState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          uav_interfaces__msg__EgoState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!uav_interfaces__msg__EgoState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
