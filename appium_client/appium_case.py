from unittest.case import TestCase
from .device.device import DEVICE_LIST
from .console_utils import logi
import os


class AppiumCase(TestCase):
    app_package = None
    app_activity = None

    def __init__(self, _driver, *args, **kwargs):
        super(AppiumCase, self).__init__(*args, **kwargs)
        self.driver = self.init_driver()

    # @classmethod
    # def setUp(cls):
    #     logi('set up case...')
    #     cls.driver = cls.init_driver()
    #     if cls.driver.current_activity != cls.app_activity:
    #         command = "am start -W %s/%s" % (cls.app_package, cls.app_activity)
    #         os.system(command)

    def setUp(self):
        logi('set up case...')
        if self.driver.current_activity != self.app_activity:
            command = "am start -W %s/%s" % (self.app_package, self.app_activity)
            os.system(command)

    @classmethod
    def init_driver(cls):
        if DEVICE_LIST:
            return DEVICE_LIST[0]



