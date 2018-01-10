from .appium_server import AppiumServer
from .console_utils import log_printer
from .device.device import Device
from .console_utils import logi
from collections import namedtuple
from conf import CASE_DIR, RESULT_DIR
import sys
import os
import time


TestCaseObject = namedtuple('TestCaseObject', ['device_type', 'module_object', 'case_name', 'app_name'])
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


def init_device(_device_list):
    _result = dict()
    if not isinstance(_device_list, dict):
        raise(TypeError('device list must be a dictionary.'))
    for _device_type, _device_id in _device_list.items():
        _device_obj = Device(_device_id[0])
        if _device_type in _result:
            _result[_device_type].append(_device_obj)
        else:
            _result[_device_type] = [_device_obj,]
    print_device_list(_result)
    return _result

def print_device_list(_device_list):
    logi('-'*20 + 'Devices Lists' + '-'*20)
    for _device_type, _type_list in _device_list.items():
        logi('{}: {}'.format(_device_type, _type_list[0]))

def off_all_devices(_device_object_list):
    for each_type in _device_object_list.values():
        for each in each_type:
            each.stop()

class AppiumClient(object):
    def __init__(self, _device_list):
        # 测试集
        self.test_suite = None
        # 初始化设备列表
        self.device_list = init_device(_device_list)

    def run(self, _test_case_dict):
        # 获取合法的待测试用例集
        self.test_suite = self._build_test_suite(_test_case_dict)
        # begin
        _log_dir = get_log_dir()

        for each_case in self.test_suite:
            _device_type = each_case.device_type
            if not _device_type in self.device_list:
                raise(NameError('device type name error: {}'.format(_device_type)))
            if not self.device_list[_device_type]:
                raise(ValueError('{} don\'t have enough device'.format(_device_type)))

            _device_object = self.device_list[_device_type][0]
            _device_object.bind(each_case)
            each_case.module_object(
                _device_object=_device_object,
                _case_name=each_case.case_name,
                _log_dir=_log_dir
            ).run_test()

        # after all
        self.stop()

    def stop(self):
        off_all_devices(self.device_list)

    @staticmethod
    @log_printer('BUILD test suite ... ')
    def _build_test_suite(_test_case_dict):
        """ 构建测试用例集并封装成合适形式 """
        _result = list()
        for _each_device, _app_list in _test_case_dict.items():
            for _app_name, _case_list in _app_list.items():
                # 处理设备
                for _each_case in _case_list:
                    try:
                        _case_class = import_class(_each_case)
                    except ImportError:
                        raise ImportError('{} is not found.'.format(_each_case))
                    else:
                        _result.append(
                            TestCaseObject(
                                _each_device,
                                _case_class,
                                _each_case,
                                _each_device + _app_name
                            )
                        )
        return _result

