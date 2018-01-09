from .base_page_test_case import BasePageTestCase


class Case1(BasePageTestCase):
    def test_case1(self):
        print('case 1 running!')
        self.driver.swipe(100, 100, 200, 200, 500)
        self.assertTrue(True)
