from cases.base_test_case import BaseTestCase


class BaseAppTestCase(BaseTestCase):
    def __init__(self, _driver):
        super(BaseAppTestCase, self).__init__(_driver)
