from .console_utils import logi, log_printer, timer, import_class
from .report_generator.report_generator import markdown2html
from conf import API_DIR
from collections import namedtuple
import traceback
import os

ReportObject = namedtuple('ReportObject', ['case_name', 'status', 'traceback', 'screenshot'])


def module_to_class_name(_name):
    for i, _letter in enumerate(list(_name)):
        if _letter == '_':
            _name[i+1] = _name[i+1].upper()
    return _name.replace('_', '')


class AppiumCase(object):
    app_package = None
    app_activity = None

    def __init__(self, _device_object, _case_name, _log_dir, _app_name):
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
        self.__init_app()
        # 导入API
        self.api = self.__init_api(_app_name)

        #
        self.__screenshot = None
        self.__traceback = None

    @staticmethod
    def __init_api(_app_name):
        # TODO: 考虑api的加载策略
        _api_path = '{}.{}.{}.{}'.format(
            API_DIR, _app_name,
            _app_name, module_to_class_name(_app_name)
        )
        try:
            return import_class(_api_path)
        except ImportError:
            raise (ImportError('{} not existed.'.format(_api_path)))

    def __init_app(self):
        """ 到达目标应用的目标页面 """
        self.device.adb.shell("am start -W %s/%s" % (self.app_package, self.app_activity))

    @timer
    def __run_test(self):
        """ 执行用例的流程 """
        logi('Start case: {}'.format(self.case_name))
        try:
            self.prepare()
            self.run()
        except:
            self.__deal_with_exception()
        else:
            self.__finish()
        finally:
            markdown2html(
                ReportObject(
                    self.case_name,
                    self.__status,
                    self.__traceback,
                    self.__screenshot
                ),
                os.path.join(self.case_log_dir, 'result.html')
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

    def __deal_with_exception(self):
        # TODO: anr log/ all log/ console log
        self.__status = False

        self.__screenshot = os.path.join(self.case_log_dir, 'screenshot.png')
        self.__traceback = traceback.print_exc()

        self.device.get_screen_shot(self.__screenshot)
        traceback.print_exc(file=open(os.path.join(self.case_log_dir, 'traceback.txt'), 'w+'))

    def __finish(self):
        # no error end
        self.__status = True
