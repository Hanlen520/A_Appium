import subprocess
from .appium import webdriver
from .console_utils import log_printer


SERVER_COMMAND = ' appium -p {port} -bp {bootstrap_port} -U {device_id} --local-timezone  --command-timeout 1200 --log-timestamp  --session-override '
PORT_LIST = list(range(25000, 26000))
BOOTSTRAP_PORT_LIST = list(range(26001, 27000))

class AppiumServer(object):
    def __init__(self, case_object):
        #
        self.desired_caps = self._get_desire_caps(case_object)
        # 服务端子进程对象
        self._server_process = None
        #
        self._driver = None

    def _get_desire_caps(self, _case_object):
        _desired_caps = dict()
        _desired_caps['deviceName'] = '{}-{}'.format(
            _case_object.device_object.device_id,
            _case_object.device_object.device_name
        )
        _desired_caps['platformName'] = 'Android'
        _desired_caps['platformVersion'] = _case_object.device_object.system_version
        _desired_caps['appPackage'] = _case_object.module_object.app_package
        _desired_caps['appActivity'] = _case_object.module_object.app_activity
        _desired_caps['dontStopAppOnReset'] = True
        _desired_caps['noReset'] = True
        _desired_caps['stopAppAtEnd'] = False
        _desired_caps['autoUnlock'] = False
        _desired_caps['newCommandTimeout'] = 600

        return _desired_caps

    @log_printer('START server ...')
    def start(self):
        """ 启动服务端 """
        port_num = PORT_LIST.pop(),
        bootstrap_port_num = BOOTSTRAP_PORT_LIST.pop(),

        _cmd = SERVER_COMMAND.format(
            port = port_num[0],
            bootstrap_port = bootstrap_port_num[0],
            device_id = self.desired_caps['deviceName'].split('-')[0]
        )
        self._server_process = subprocess.Popen(_cmd, shell=True)
        return self._get_driver(port_num[0])

    @log_printer('STOP server ...')
    def stop(self):
        """ 停止服务端 """
        self._server_process.terminate()
        self._driver.quit()

    def _get_driver(self, port_num):
        """ 获取driver对象 """
        self._driver = webdriver.Remote(
            'http://localhost:{}/wd/hub'.format(port_num),
            self.desired_caps)
        return self._driver