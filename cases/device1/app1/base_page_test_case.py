from cases.device1.base_app_test_case import BaseAppTestCase


class BasePageTestCase(BaseAppTestCase):
    app_package = 'com.cyanogenmod.trebuchet'
    app_activity = 'com.android.launcher3.Launcher'

    def __init__(self, _driver):
        super(BasePageTestCase, self).__init__(_driver)

