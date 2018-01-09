from .base_page_test_case import BasePageTestCase


class Case1(BasePageTestCase):
    def test_case1(self):
        print('case 1 running!')
        self.driver.swipe(100, 100, 200, 200, 500)
        assert(True)

    def run_test(self, *args, **kwargs):
        super(Case1, self).run_test(*args, **kwargs)
        self.test_case1()