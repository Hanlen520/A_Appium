from .device.device import DEVICE_LIST
from .console_utils import logi, log_printer
import sys


class AppiumCase(object):
    app_package = None
    app_activity = None

    def __init__(self):
        self.device = None
        self.driver = None

    def init_app(self):
        self.device.adb.shell("am start -W %s/%s" % (self.app_package, self.app_activity))

    def run_test(self, _device_object, _driver):
        self.device = _device_object
        self.driver = _driver
        self.init_app()



