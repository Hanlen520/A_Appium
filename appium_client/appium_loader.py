""" 一个自定义的、继承自defaultTestLoader的loader，将打包出来的形式变更为AppiumSuite对象 """
import unittest
import warnings
import traceback
from .appium_suite import AppiumSuite

case = unittest.case


class _FailedTest(case.TestCase):
    _testMethodName = None

    def __init__(self, method_name, exception):
        self._exception = exception
        super(_FailedTest, self).__init__(method_name)

    def __getattr__(self, name):
        if name != self._testMethodName:
            # return super(_FailedTest, self).__getattr__(name)
            return getattr(super(_FailedTest, self), name)
        def testFailure():
            raise self._exception
        return testFailure


def _make_failed_test(methodname, exception, suiteClass, message):
    test = _FailedTest(methodname, exception)
    return suiteClass((test,)), message


def _make_failed_load_tests(name, exception, suiteClass):
    message = 'Failed to call load_tests:\n%s' % (traceback.format_exc(),)
    return _make_failed_test(
        name, exception, suiteClass, message)


class AppiumLoader(unittest.defaultTestLoader):
    suiteClass = AppiumSuite

    def __init__(self, *args, **kwargs):
        super(AppiumLoader, self).__init__(*args, **kwargs)

    def loadTestsFromModule(self, module, *args, pattern=None, **kws):
        """Return a suite of all test cases contained in the given module"""
        # This method used to take an undocumented and unofficial
        # use_load_tests argument.  For backward compatibility, we still
        # accept the argument (which can also be the first position) but we
        # ignore it and issue a deprecation warning if it's present.
        if len(args) > 0 or 'use_load_tests' in kws:
            warnings.warn('use_load_tests is deprecated and ignored',
                          DeprecationWarning)
            kws.pop('use_load_tests', None)
        if len(args) > 1:
            # Complain about the number of arguments, but don't forget the
            # required `module` argument.
            complaint = len(args) + 1
            raise TypeError('loadTestsFromModule() takes 1 positional argument but {} were given'.format(complaint))
        if len(kws) != 0:
            # Since the keyword arguments are unsorted (see PEP 468), just
            # pick the alphabetically sorted first argument to complain about,
            # if multiple were given.  At least the error message will be
            # predictable.
            complaint = sorted(kws)[0]
            raise TypeError("loadTestsFromModule() got an unexpected keyword argument '{}'".format(complaint))
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, case.TestCase):
                tests.append(self.loadTestsFromTestCase(obj))

        load_tests = getattr(module, 'load_tests', None)
        tests = self.suiteClass(tests)
        if load_tests is not None:
            try:
                return load_tests(self, tests, pattern)
            except Exception as e:
                error_case, error_message = _make_failed_load_tests(
                    module.__name__, e, self.suiteClass)
                self.errors.append(error_message)
                return error_case
        return tests