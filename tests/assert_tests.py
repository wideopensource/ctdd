from ctdd import Tester

class BootstrapTests(Tester):
    def test_sut_compiles(self):
        self.assertIsNotNone(self.sut)


class AssertTests(Tester):
    def test_assertZero_raises_with_non_zero(self):
        with self.assertRaises(AssertionError):
            self.assertZero(2)

    def test_assertZero_does_not_raises_with_zero(self):
        with self.assertDoesNotRaise():
            self.assertZero(0)

Tester.go()
