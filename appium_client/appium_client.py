from .appium_server import AppiumServer
from .console_utils import log_printer
from .device.device import Device
from .console_utils import logi
from collections import namedtuple
from conf import CASE_DIR, RESULT_DIR
import sys
import os
import time


TestCaseObject = namedtuple('TestCaseObject', ['device_object', 'module_object', 'case_name'])
sys.path.insert(0, os.path.abspath(CASE_DIR))


def import_class(import_str):
    """ Returns a class from a string including module and class. """
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class {} cannot be found'.format(class_str))


def get_log_dir():
    _dir_path = os.path.abspath(
        os.path.join(
            RESULT_DIR, 'RESULT'+str(time.time()).split('.')[0]
        )
    )
    if not os.path.exists(_dir_path):
        os.mkdir(_dir_path)
    return _dir_path


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
        _log_dir = get_log_dir()

        for each_case in self.test_suite:
            # TODO: 同一个应用中不需要重复开服务
            self.server = AppiumServer(each_case)
            self.driver = self.server.start()
            each_case.module_object(
                _device_object=each_case.device_object,
                _driver=self.driver,
                _case_name=each_case.case_name,
                _log_dir=_log_dir
            ).run_test()
            self.stop()

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


