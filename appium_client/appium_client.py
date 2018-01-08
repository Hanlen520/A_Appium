from .appium_server import AppiumServer
from .console_utils import log_printer
from .htmltestrunner_py3 import HTMLTestRunner
from .device.device import Device
from collections import namedtuple
from conf import CASE_PATH, RESULT_PATH
from appium_client.appium_suite import AppiumSuite
import unittest
import traceback
import sys
import os


TestCaseObject = namedtuple('TestCaseObject', ['device_object', 'module_object'])
sys.path.insert(0, os.path.abspath(CASE_PATH))

class AppiumClient(object):
    def __init__(self, _device_list):
        # 服务端对象
        self.server = None
        # 驱动
        self.driver = None
        # 执行测试的引擎
        self.runner = self._get_runner(RESULT_PATH)
        # 测试集
        self.test_suite = None

    def run(self, _test_case_dict):
        try:
            # 获取合法的待测试用例集
            self.test_suite = self._build_test_suite(_test_case_dict)
            # begin
            for each_case in self.test_suite:
                self.server = _server_object = AppiumServer(each_case)
                self.driver = _server_object.start()
                _test_case = self._load_case(each_case.module_object)
                _test_case = AppiumSuite(_test_case)
                # TODO: runner里面配置log位置和conf等, 需要一系列调整
                self.runner.run(_test_case)
        except Exception:
            print(traceback.print_exc())
        finally:
            # stop
            self.stop()

    def stop(self):
        self.server.stop()
        # self.driver.quit()

    @staticmethod
    @log_printer('BUILD test suite ... ')
    def _build_test_suite(_test_case_dict):
        _result = list()
        for _each_device, _test_case_list in _test_case_dict.items():
            for _each_case in _test_case_list:
                try:
                    _case_class = AppiumClient.import_class(_each_case)
                except ImportError:
                    raise ImportError('{} is not found.'.format(_each_case))
                else:
                    _result.append(TestCaseObject(Device(_each_device), _case_class))
        return _result

    def _load_case(self, _module_object):
        return unittest.defaultTestLoader.loadTestsFromModule(_module_object)

    @staticmethod
    def import_class(import_str):
        """ Returns a class from a string including module and class. """
        mod_str, _sep, class_str = import_str.rpartition('.')
        __import__(mod_str)
        try:
            return getattr(sys.modules[mod_str], class_str)
        except AttributeError:
            raise ImportError('Class {} cannot be found'.format(class_str))

    @staticmethod
    def _get_runner(log_dir):
        """
        获取HTMLTestRunner实例.
        HTMLTestRunner对unittest进行了封装, 能够在测试执行后生成html格式的报告.
        执行用例的部分依旧沿用unittest.
        """
        import time
        report_file = os.path.join(log_dir, "{}.html".format(str(time.time()).split('.')[0]))
        fp = open(report_file, 'wb')
        # report file path, title
        runner = HTMLTestRunner(
            stream=fp,
            title='abc'
        )
        return runner