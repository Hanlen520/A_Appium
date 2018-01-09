from cases.base_test_case import BaseTestCase


class BaseAppTestCase(BaseTestCase):
    app_package = 'com.google.android.apps.photos'
    app_activity = '.home.HomeActivity'
