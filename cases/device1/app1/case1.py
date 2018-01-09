from ..base_app_test_case import BaseAppTestCase


class Case1(BaseAppTestCase):
    def test_case1(self):
        print('case 1 running!')
        self.driver.swipe(100, 100, 200, 200, 500)
        assert(True)

    def run_test(self, *args, **kwargs):
        super(Case1, self).run_test(*args, **kwargs)
        self.test_case1()