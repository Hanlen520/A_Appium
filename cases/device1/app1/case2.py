from .base_page_test_case import BasePageTestCase


class Case2(BasePageTestCase):
    def test_case2(self):
        self.driver.swipe(100, 100, 200, 200, 500)
