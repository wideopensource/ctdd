from john import TestCase
from .tester_state import TesterState

class Tester(TestCase):
    _state = None
    factory = None
    _source_files = []
    _header_files = []
    _include_paths = []

    @staticmethod
    def _ensure_state(verbose=False):
        if not Tester._state:
            Tester._state = TesterState('__main__', 
                                        Tester._source_files, 
                                        Tester._header_files, 
                                        Tester._include_paths, 
                                        verbose=verbose)
            Tester.factory = Tester._state.factory

        return Tester

    @staticmethod
    def help():
        Tester._ensure_state()

        print(f"Tester: {[x for x in dir(Tester) if not x.startswith('_')]}")
        print(f"factory: {[x for x in dir(Tester.factory) if not x.startswith('_')]}")
        print(f"externs: {[x for x in Tester._state.externs if not x.startswith('_')]}")

        return Tester

    @classmethod
    def tearDownClass(cls) -> None:
        print(f'\r                              ', end='')
        return super().tearDownClass()

    @staticmethod
    def addSourceFile(filename):
        Tester._source_files.append(filename)
        return Tester

    @staticmethod
    def addHeaderFile(filename):
        Tester._header_files.append(filename)
        return Tester

    @staticmethod
    def addIncludePath(filename):
        Tester._include_paths.append(filename)
        return Tester

    @staticmethod
    def go(verbose=False):
        Tester._ensure_state(verbose=verbose).Runner.run()
        return Tester

    @property
    def sut(self):
        return Tester._state.ensure_sut()

    def __init__(self, method_name:str):
        super().__init__(method_name)

        test_name = self.id()
        if test_name.startswith('__main__.'):
            test_name = test_name[9:]

        self.test_name = test_name

    def setup(self):
        pass

    def teardown(self):
        pass

    def setUp(self):
        super().setUp()
        self._state.ensure_sut()
        print(f'\r> -- {self.test_name} --')
        self.setup()
        self._state.mocker.clear()

    def tearDown(self):
        super().tearDown()
        self.teardown()
        self._state.mocker.print_all()
        print(f'< ---{"".ljust(len(self.test_name), "-")}---')

    def assertStrEqual(self, expected, actual):
        if not isinstance(actual, str):
            actual = self.sut.str(actual)

        self.assertEqual(actual, expected)

    def assertNotCalled(self, func):
        self.assertZero(self._state.mocker.get_number_of_calls(func))

    def assertCalled(self, func):
        self.assertNotZero(self._state.mocker.get_number_of_calls(func))

    def assertCalledOnce(self, func):
        self.assertEqual(1, self._state.mocker.get_number_of_calls(func))

    def assertCalledTwice(self, func):
        self.assertEqual(2, self._state.mocker.get_number_of_calls(func))

