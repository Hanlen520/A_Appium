from ..base_app_test_case import BaseAppTestCase


class Case1(BaseAppTestCase):
    def test_case1(self):
        print('case 1 running!')
        self.driver.swipe(100, 100, 200, 200, 500)
        assert(False)

    def run(self):
        self.test_case1()