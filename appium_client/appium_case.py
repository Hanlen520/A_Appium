from .console_utils import logi
import traceback


class AppiumCase(object):
    app_package = None
    app_activity = None

    def __init__(self, _device_object, _driver):
        self.device = None
        self.driver = None
        self.logi = logi

        self.device = _device_object
        self.driver = _driver
        self.init_app()

    def init_app(self):
        """ 到达目标应用的目标页面 """
        self.device.adb.shell("am start -W %s/%s" % (self.app_package, self.app_activity))

    def run_test(self):
        """ 执行用例的流程 """
        try:
            self.prepare()
            self.run()
        except:
            traceback.print_exc()
            # TODO: 截图、log抓取、log打印
            # 可以直接打印到文件里
            # traceback.print_exc(file='something')
        finally:
            self.clean_up()

    def prepare(self):
        pass

    def clean_up(self):
        pass

    def run(self):
        """ 在用例中重写这个函数以安排测试入口 """
        pass
