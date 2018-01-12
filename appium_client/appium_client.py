from .report_generator.report_generator import ReportGenerator
from .console_utils import log_printer
from .device.device import Device
from .console_utils import logi, import_class
from collections import namedtuple
from conf import CASE_DIR, RESULT_DIR, WAIT_TIME
import sys
import os
import time

# 用例对象，包含：设备类型、用例模块对象、用例名称、应用名称
TestCaseObject = namedtuple('TestCaseObject', ['device_type', 'module_object', 'case_name', 'app_name'])
sys.path.insert(0, os.path.abspath(CASE_DIR))


def get_log_dir():
    """ 获取生成结果的目标文件夹位置 """
    _dir_path = os.path.abspath(
        os.path.join(
            RESULT_DIR, 'RESULT'+str(time.time()).split('.')[0]
        )
    )
    if not os.path.exists(_dir_path):
        os.mkdir(_dir_path)
    return _dir_path


def init_device(_device_list):
    """ 初始化设备队列 """
    _result = dict()
    if not isinstance(_device_list, dict):
        raise(TypeError('device list must be a dictionary.'))
    for _device_type, _device_id in _device_list.items():
        for _each_device in _device_id:
            _device_obj = Device(_each_device)
            if _device_type in _result:
                _result[_device_type].append(_device_obj)
            else:
                _result[_device_type] = [_device_obj,]
    print_device_list(_result)
    return _result


def print_device_list(_device_list):
    """ 展示现有设备队列 """
    logi('Device List'.center(40, '-'))
    for _device_type, _type_list in _device_list.items():
        logi('{}: {}'.format(_device_type, _type_list[0]))
    logi('End'.center(40, '-'))


def off_all_devices(_device_object_list):
    """ 停止所有设备 """
    for each_type in _device_object_list.values():
        for each in each_type:
            each.stop()


class AppiumClient(object):
    def __init__(self, _device_list):
        # 测试集
        self.test_suite = None
        # 初始化设备列表
        self.device_list = init_device(_device_list)
        # 报告制作
        self.report_generator = None

    def run(self, _test_case_dict):
        # 获取合法的待测试用例集
        self.test_suite = self._build_test_suite(_test_case_dict)
        # 获取目标位置
        _log_dir = get_log_dir()
        # 初始化报告生成器
        self.report_generator = ReportGenerator(os.path.join(_log_dir, 'result.rst'))
        # 开始测试
        for each_case in self.test_suite:
            # 检查设备的合法性
            _device_type = each_case.device_type
            if _device_type not in self.device_list:
                raise(NameError('device type name error: {}'.format(_device_type)))
            if not self.device_list[_device_type]:
                raise(ValueError('{} don\'t have enough device'.format(_device_type)))

            # 默认取第一台设备作为主测机
            _device_object = self.device_list[_device_type][0]
            _device_object.bind(each_case)

            # 向appium_case对象传入参数，开始测试
            each_case.module_object(
                _device_object=_device_object,
                _case_name=each_case.case_name,
                _log_dir=_log_dir,
                _app_name=each_case.app_name,
                _report_generator=self.report_generator
            ).run_test()

            # 每轮测试过后的等待时间
            time.sleep(WAIT_TIME)

        # after all
        self.report_generator.build()
        self.stop()

    def stop(self):
        # 停止时断开所有设备，关闭他们对应的server
        off_all_devices(self.device_list)

    @staticmethod
    @log_printer('build test suite')
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
                                _each_device + '.' + _app_name
                            )
                        )
        return _result

