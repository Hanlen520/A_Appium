import unittest.test.test_case as test_case


class AppiumCase(test_case):
    def __init__(self, _driver):
        super(AppiumCase, self).__init__()
        self.driver = _driver