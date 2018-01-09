from .appium_server import AppiumServer
from .console_utils import log_printer
from .device.device import Device
from .console_utils import logi
from collections import namedtuple
from conf import CASE_PATH
import sys
import os
import time


TestCaseObject = namedtuple('TestCaseObject', ['device_object', 'module_object', 'class_name'])
sys.path.insert(0, os.path.abspath(CASE_PATH))


def import_class(import_str):
    """ Returns a class from a string including module and class. """
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class {} cannot be found'.format(class_str))


class AppiumClient(object):
    def __init__(self, _device_list):
        # 服务端对象
        self.server = None
        # 驱动
        self.driver = None
        # 测试集
        self.test_suite = None

    def run(self, _test_case_dict):
        # 获取合法的待测试用例集
        self.test_suite = self._build_test_suite(_test_case_dict)
        # begin
        for each_case in self.test_suite:
            # timer
            _start_time = time.time()
            logi('START test: {}'.format(each_case.class_name))
            # TODO: 同一个应用中不需要重复开服务
            self.server = AppiumServer(each_case)
            self.driver = self.server.start()
            each_case.module_object(
                _device_object=each_case.device_object,
                _driver=self.driver
            ).run_test()
            self.stop()

            logi('DONE in {}s'.format(round(time.time() - _start_time, 2)))

    def stop(self):
        self.server.stop()

    @staticmethod
    @log_printer('BUILD test suite ... ')
    def _build_test_suite(_test_case_dict):
        """ 构建测试用例集并封装成合适形式 """
        _result = list()
        for _each_device, _test_case_list in _test_case_dict.items():
            for _each_case in _test_case_list:
                # TODO： 在此处一并完成API的载入
                try:
                    _case_class = import_class(_each_case)
                except ImportError:
                    raise ImportError('{} is not found.'.format(_each_case))
                else:
                    _result.append(TestCaseObject(Device(_each_device), _case_class, _each_case))
        return _result

    def load_case(self, _module_object):
        """ 读取测试用例并将其转换为testsuite形式 """
        import unittest
        return unittest.defaultTestLoader.loadTestsFromModule(_module_object)

