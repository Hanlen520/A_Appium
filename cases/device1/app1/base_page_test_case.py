from cases.device1.base_app_test_case import BaseAppTestCase


class BasePageTestCase(BaseAppTestCase):
    app_package = 'com.google.android.apps.photos'
    app_activity = '.home.HomeActivity'


