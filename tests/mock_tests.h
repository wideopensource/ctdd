#pragma once

typedef char const *(*char_const_ptr_callback_t)();

struct char_const_ptr_callback_data_t
{
    char_const_ptr_callback_t callback;
};

int test_char_const_ptr_callback_with_hello(struct char_const_ptr_callback_data_t *data);