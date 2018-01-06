from .appium_server import AppiumServer
from .device.device import Device
from .htmltestrunner_py3 import HTMLTestRunner
from collections import namedtuple

TestCaseObject = namedtuple('TestCaseObject', ['device_id', 'module_name'])


class AppiumClient(object):
    def __init__(self, _device_list):
        # 配置设备字典
        self._device_list = _device_list
        # 服务端对象
        self.server = None
        # 驱动
        self.driver = None
        # 执行测试的引擎
        self.runner = HTMLTestRunner
        # 测试集
        self.test_suite = None

    def run(self, _test_case_dict):
        # 获取合法的待测试用例集
        self.test_suite = self._build_test_suite(_test_case_dict)
        # begin
        for each_case in self.test_suite:
            _driver = AppiumServer(each_case).start()
            # TODO：看一下HTMLTESTRUNNER这里面是怎么运作的
            HTMLTestRunner.run(each_case, _driver)

        #
        self.stop()

    def stop(self):
        self.server.stop()
        self.driver.quit()

    @staticmethod
    def _build_test_suite(_test_case_dict):
        _result = list()
        for _each_device, _test_case_list in _test_case_dict.items():
            for _each_case in _test_case_list:
                try:
                    _case_class = __import__(_each_case)
                except ImportError:
                    raise ImportError('{} is not found.'.format(_each_case))
                else:
                    _result.append(TestCaseObject(_each_device, _case_class))
        return _result

    @staticmethod
    def _confirm_device_connected(_device_id):
        # todo: use adb
        pass

    @staticmethod
    def _build_device_object(_device_id):
        pass
