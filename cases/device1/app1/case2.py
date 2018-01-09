from .base_page_test_case import BasePageTestCase


class Case2(BasePageTestCase):
    def test_case2(self):
        from appium_client.console_utils import logi
        logi('case1 running~')
        self.driver.swipe(100, 100, 200, 200, 500)
        self.assertTrue(True)

