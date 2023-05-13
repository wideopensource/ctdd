from ctdd import Tester

class MockReturnTests(Tester):
    def test_char_const_ptr(self):
        return_value = self.factory.C_string('hello')
        data = self.factory.char_const_ptr_callback_data_t()
        data.callback = self.factory.char_const_ptr_callback_t(return_value)

        result = self.sut.test_char_const_ptr_callback_with_hello(data)

        self.assertCalled(0)
        self.assertTrue(result)


Tester.go()
