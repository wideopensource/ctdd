#pragma once

typedef char const *(*char_const_ptr_callback_t)();

struct char_const_ptr_callback_data_t
{
    char_const_ptr_callback_t callback;
};

int test_char_const_ptr_callback_with_hello(struct char_const_ptr_callback_data_t *data);

typedef void (*simple_func_t)();
void set_simple_func(simple_func_t);
void run_simple_func();

typedef int (*returning_func_t)();
void set_returning_func(returning_func_t);
int run_returning_func();