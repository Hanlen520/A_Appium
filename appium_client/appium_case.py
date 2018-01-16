"""
所有api的基类
"""
from .console_utils import logi, log_printer, timer, import_class, module_to_class_name
from conf import API_DIR
from collections import namedtuple
import traceback
import os
import time

ReportObject = namedtuple('ReportObject', ['case_name', 'status', 'traceback', 'screenshot', 'time_cost'])


class AppiumCase(object):
    app_package = None
    app_activity = None

    def __init__(self, _device_object, _case_name, _log_dir, _app_name, _report_generator, _device_list):
        # driver对象
        self.driver = None
        # 方便打log
        self.logi = logi
        # Device对象
        self.device = _device_object
        # driver对象
        self.driver = _device_object.driver
        # 用例名称
        self.case_name = _case_name
        # 结果文件夹
        self.case_log_dir = os.path.join(_log_dir, self.case_name)
        # 初始化应用
        self._init_app()
        # 导入API
        self.api = self._init_api(_app_name, self.driver)
        # 报告制造
        self._report_generator = _report_generator
        # 该系列设备列表
        self.device_list = _device_list

        # 使用其他设备
        # other_driver = self.device_list[1].driver

        # 截图与traceback
        self._screenshot = None
        self._traceback = None

    @log_printer('preparing ...')
    def prepare(self):
        """ 测试前的准备 """
        pass

    @log_printer('cleaning up ...')
    def clean_up(self):
        """ 测试结束后的清理 """
        pass

    def run(self):
        """ 在用例中重写这个函数以安排测试入口 """
        pass

    @staticmethod
    def _init_api(_app_name, _driver):
        """ 初始化API """
        _device_name, _app_module_name, *_ = _app_name.split('.')
        _api_path = '{}.{}.{}.{}.{}'.format(
            API_DIR, _device_name, _app_module_name, _app_module_name,
            module_to_class_name(_app_module_name)
        )
        try:
            return import_class(_api_path)(_driver)
        except ImportError:
            raise (ImportError('{} not existed.'.format(_api_path)))

    def _init_app(self):
        """ 到达目标应用的目标页面 """
        self.device.adb.shell("am start -W %s/%s" % (self.app_package, self.app_activity))

    @log_printer('TEST'.center(40, '-'))
    @timer
    def run_test(self):
        """ 执行用例的流程 """
        _inner_timer = time.time()
        try:
            self.prepare()
            self.run()
        except:
            self._deal_with_exception()
        else:
            self._finish()
        finally:
            logi('{}: {}'.format(self.case_name, self._status))
            self._report_generator.add_section(
                ReportObject(
                    self.case_name,
                    self._status,
                    self._traceback,
                    self._screenshot,
                    str(round(time.time() - _inner_timer, 3))
                )
            )
            self.clean_up()
            self.driver.reset()

    def _deal_with_exception(self):
        # TODO: anr log/ all log/ console log
        self._status = False

        self._screenshot = os.path.join(self.case_log_dir, 'screenshot.png')
        self._traceback = traceback.format_exc()

        self.device.get_screen_shot(self._screenshot)

        with open(os.path.join(self.case_log_dir, 'traceback.txt'), 'w+') as f:
            f.write(self._traceback)

    def _finish(self):
        # no error end
        if not os.path.exists(self.case_log_dir):
            os.mkdir(self.case_log_dir)
        self._status = True
