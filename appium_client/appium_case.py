from unittest.case import TestCase


class AppiumCase(TestCase):
    def __init__(self, _driver, *args, **kwargs):
        super(AppiumCase, self).__init__(*args, **kwargs)
        self.driver = _driver
