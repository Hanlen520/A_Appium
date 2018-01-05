from .appium_server import AppiumServer
from .device.device import Device


class AppiumClient(object):
    def __init__(self, _device_conf):
        self.device = Device(_device_conf)
        self.driver = None

    def run(self):
        # 初始化server，构建driver
        self.server = AppiumServer(self.device)
        self.driver = self.server.start()

        # 开始测试
        self.start()
        self.stop()

    def start(self):
        # TODO: use cases
        # do something
        self.driver.swipe(100, 100, 200, 200, 500)

    def stop(self):
        self.server.stop()
        self.driver.quit()
