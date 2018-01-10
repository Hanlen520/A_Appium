from .console_utils import logi, log_printer, timer
import traceback
import os


class AppiumCase(object):
    app_package = None
    app_activity = None

    def __init__(self, _device_object, _case_name, _log_dir):
        self.device = None
        self.driver = None
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
        self.init_app()

    def init_app(self):
        """ 到达目标应用的目标页面 """
        self.device.adb.shell("am start -W %s/%s" % (self.app_package, self.app_activity))

    @timer
    def run_test(self):
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
            self.clean_up()
            self.driver.reset()

    @log_printer('preparing ...')
    def prepare(self):
        pass

    @log_printer('cleaning up ...')
    def clean_up(self):
        pass

    @log_printer('start test ...')
    def run(self):
        """ 在用例中重写这个函数以安排测试入口 """
        pass

    def __deal_with_exception(self):
        # TODO: anr log/ all log/ console log
        self.device.get_screen_shot(os.path.join(self.case_log_dir, 'screenshot.png'))
        traceback.print_exc(file=open(os.path.join(self.case_log_dir, 'traceback.txt'), 'w+'))

    def __finish(self):
        # no error end
        pass

