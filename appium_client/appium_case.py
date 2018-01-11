from .console_utils import logi, log_printer, timer, import_class
from conf import API_DIR
from collections import namedtuple
import traceback
import os

ReportObject = namedtuple('ReportObject', ['case_name', 'status', 'traceback', 'screenshot'])


def module_to_class_name(_name):
    _name = _name.capitalize()
    for i, _letter in enumerate(list(_name)):
        if _letter == '_':
            _name[i+1] = _name[i+1].upper()
    return _name.replace('_', '')


class AppiumCase(object):
    app_package = None
    app_activity = None

    def __init__(self, _device_object, _case_name, _log_dir, _app_name, _report_generator):
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

        #
        self._screenshot = None
        self._traceback = None

    @staticmethod
    def _init_api(_app_name, _driver):
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
    def _run_test(self):
        """ 执行用例的流程 """
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
                    self._screenshot
                )
            )
            self.clean_up()
            self.driver.reset()

    @log_printer('preparing ...')
    def prepare(self):
        pass

    @log_printer('cleaning up ...')
    def clean_up(self):
        pass

    def run(self):
        """ 在用例中重写这个函数以安排测试入口 """
        pass

    def _deal_with_exception(self):
        # TODO: anr log/ all log/ console log
        self._status = False

        self._screenshot = os.path.join(self.case_log_dir, 'screenshot.png')
        self._traceback = traceback.print_exc()

        self.device.get_screen_shot(self._screenshot)
        traceback.print_exc(file=open(os.path.join(self.case_log_dir, 'traceback.txt'), 'w+'))

    def _finish(self):
        # no error end
        self._status = True
