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