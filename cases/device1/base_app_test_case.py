from ..base_test_case import BaseTestCase


class BaseAppTestCase(BaseTestCase):
    def __init__(self, _driver):
        super(BaseAppTestCase, self).__init__(_driver)
        self.app_package = 'com.cyanogenmod.trebuchet'
        self.app_activity = 'com.android.launcher3.Launcher'
