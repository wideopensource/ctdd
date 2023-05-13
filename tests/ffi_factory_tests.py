from ctdd import Tester, FFIFactory

class FFIFactoryTests(Tester):
    def test_null_pointer_no_ffi_raises(self):
        sut = FFIFactory()
        
        with self.assertRaises(RuntimeError):
            sut.null_pointer

    def test_new_no_ffi_raises(self):
        sut = FFIFactory()
        
        with self.assertRaises(RuntimeError):
            sut.C_int(42)

class FFIFactoryPrimitiveTests(Tester):
    def test_C_string(self):
        s = self.factory.C_string('hello')

        self.assertEqual(b'h', s[0])
        self.assertEqual(b'e', s[1])
        self.assertEqual(b'l', s[2])
        self.assertEqual(b'l', s[3])
        self.assertEqual(b'o', s[4])
        self.assertEqual(b'\x00', s[5])

        with self.assertRaisesAny():
            s[6]

    def test_P_str(self):
        s = self.factory.C_string('hello')

        self.assertStrEqual('hello', self.factory.P_str(s))

    def test_int(self):
        expected = 42

        array = self.factory.C_int(expected)
        actual = array[0]

        self.assertEqual(expected, actual)

        with self.assertRaisesAny():
            array[1]

    def test_int_array(self):
        array = self.factory.C_int_array(4)
        
        with self.assertDoesNotRaise():
            array[0]
            array[1]
            array[2]
            array[3]

        with self.assertRaisesAny():
            array[4]

    def test_initialised_int_array(self):
        expected = (42, -13)
        array = self.factory.C_int_array(expected)

        actual = (array[0], array[1],)

        self.assertEqual(expected, actual)

        with self.assertRaisesAny():
            array[2]

    def test_P_tuple(self):
        expected = (42, -13, 1729)
        array = self.factory.C_int_array(expected)

        actual = self.factory.P_tuple(array, len(expected))

        self.assertEqual(expected, actual)

    def test_int_bad_init_returns_None(self):
        result = self.factory.C_int_array('abc')

        self.assertIsNone(result)



Tester.go()
