from .base_page_test_case import BasePageTestCase


class Case1(BasePageTestCase):
    def test_case1(self):
        self.driver.swipe(100, 100, 200, 200, 500)
