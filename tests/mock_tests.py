from ctdd import Tester

class MockReturnTests(Tester):
    def test_char_const_ptr(self):
        return_value = self.factory.C_string('hello')
        data = self.factory.char_const_ptr_callback_data_t()
        data.callback = self.factory.char_const_ptr_callback_t(rv=return_value)

        result = self.sut.test_char_const_ptr_callback_with_hello(data)

        self.assertCalled(0)
        self.assertTrue(result)

    def test_simple_mock_runs(self):
        func = self.factory.simple_func_t()
        self.sut.set_simple_func(func)

        self.sut.run_simple_func()

        self.assertCalledOnce(0)   

    def test_simple_mock_called_twice(self):
        func = self.factory.simple_func_t()
        self.sut.set_simple_func(func)

        self.sut.run_simple_func()
        self.sut.run_simple_func()

        self.assertCalledTwice(0)   

    def test_returning_mock_returns(self):
        expected = 42

        func = self.factory.returning_func_t(rv=expected)
        self.sut.set_returning_func(func)

        actual = self.sut.run_returning_func()

        self.assertCalledOnce(0)   
        self.assertEqual(expected, actual)

    @staticmethod
    def mock_func() -> int:
        print(f'mock')
        return 42
    
    def test_python_mock_runs(self):
        func = self.factory.returning_func_t(target=MockReturnTests.mock_func)

        self.sut.set_returning_func(func)

        self.sut.run_returning_func()

        self.assertCalledOnce(MockReturnTests.mock_func)   

Tester.go()
