# cttd

### tl:dr

C test-driven development framework implemented in Python.

# Example

See __main__.py, __main__.c and __main__.h in the root of the repo, reproduced here (possibly out of date):

```
from cttd import Tester

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
```

```
#pragma once

int add3(int a, int b, int c);
```

```
#include "__main__.h"

int add3(int a, int b, int c)
{
    return a + b + c;
}
```
