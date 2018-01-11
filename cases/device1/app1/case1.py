from ..base_app_test_case import BaseAppTestCase


class Case1(BaseAppTestCase):
    def test_case1(self):
        self.api.page1.page1_test_api()
        self.driver.swipe(100, 100, 200, 200, 500)
        assert(False)

    def run(self):
        self.test_case1()