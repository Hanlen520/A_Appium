from .base_page_test_case import BasePageTestCase


class Case2(BasePageTestCase):
    def test_case2(self):
        from appium_client.console_utils import logi
        logi('case1 running~')
        self.driver.swipe(100, 100, 200, 200, 500)
        assert(True)

    def run_test(self, *args, **kwargs):
        super(Case2, self).run_test(*args, **kwargs)
        self.test_case2()

