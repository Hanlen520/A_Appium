from ...base_test_case import BaseTestCase


class Case1(BaseTestCase):
    def test_case1(self):
        self.driver.swipe(100, 100, 200, 200, 500)
