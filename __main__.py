from ctdd import Tester


class Add3Tests(Tester):

    def test_sut_compiles(self):
        with self.assertDoesNotRaise():
            self.sut

    def test_takes_three_f(self):
        with self.assertDoesNotRaise():
            self.sut.add3(0, 0, 0)

    def test_return_zero_for_zeros(self):
        expected = 0

        actual = self.sut.add3(0, 0, 0)

        self.assertEqual(expected, actual)

    def test_returns_sum(self):
        expected = 14

        actual = self.sut.add3(1, 4, 9)

        self.assertEqual(expected, actual)


Tester.go()
