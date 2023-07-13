#include "mock_tests.h"

#include <string.h>
#include <stdio.h>

int test_char_const_ptr_callback_with_hello(struct char_const_ptr_callback_data_t *data)
{
    char const *expected = "hello";

    char const *actual = data->callback();

    printf("in: %s\n", actual);

    return 0 == strcmp(expected, actual);
}

static simple_func_t simple_func;

void set_simple_func(simple_func_t func)
{
    simple_func = func;
}

void run_simple_func()
{
    simple_func();
}

static returning_func_t returning_func;

void set_returning_func(returning_func_t func)
{
    returning_func = func;
}

int run_returning_func()
{
    return returning_func();
}