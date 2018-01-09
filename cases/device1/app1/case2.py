from ..base_app_test_case import BaseAppTestCase
from appium_client.console_utils import logi


class Case2(BaseAppTestCase):
    def test_case2(self):
        self.driver.swipe(100, 100, 200, 200, 500)
        assert(True)

    def run(self):
        self.test_case2()

