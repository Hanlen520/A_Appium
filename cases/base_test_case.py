from appium_client.appium_case import AppiumCase


class BaseTestCase(AppiumCase):
    def __init__(self, _driver):
        super(BaseTestCase, self).__init__(_driver)
