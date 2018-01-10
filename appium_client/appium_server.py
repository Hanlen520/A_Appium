import subprocess
from .appium import webdriver
from .console_utils import log_printer, logi, kill_process
import random
import sys
import os
import time


SERVER_COMMAND = ' appium -p {port} -bp {bootstrap_port} -U {device_id} --local-timezone  --command-timeout 1200 --log-timestamp  --session-override '
PORT_LIST = list(range(25000, 26000))
BOOTSTRAP_PORT_LIST = list(range(26001, 27000))


def _is_port_using(_port_num):
    if 'linux' in sys.platform:
        port = str(_port_num)
        cmd_outer = os.popen('netstat -tunlp |grep :%s' % port).read().strip()

        if cmd_outer:
            cmd_outer_lists = cmd_outer.split('\n')

            # if port is busying,return the pid_info of port
            for line in cmd_outer_lists:
                lists = line[20:].strip().split(' ')
                if ':%s' % port in lists[0]:
                    pid_info = lists[-1].split('/')
                    return pid_info
            return False
        return False
    else:
        port = str(_port_num)

        cmd_outer = os.popen('netstat -aon |findstr :%s' % port).read().strip()

        if cmd_outer:
            cmd_outer_lists = cmd_outer.split('\n')

            # if port is busying,return the pid of port
            for line in cmd_outer_lists:
                lists = line.strip().split(' ')
                if ':%s' % port in lists[4]:
                    pid = lists[-1]
                    return pid
            return False
        return False


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
        while True:
            port_num = random.choice(PORT_LIST)
            bootstrap_port_num = random.choice(BOOTSTRAP_PORT_LIST)

            _cmd = SERVER_COMMAND.format(
                port = port_num,
                bootstrap_port = bootstrap_port_num,
                device_id = self.desired_caps['deviceName'].split('-')[0]
            )
            if not _is_port_using(port_num):
                self._server_process = subprocess.Popen(_cmd, shell=True)
                time.sleep(3)
                _driver = self._get_driver(port_num)
            else:
                logi('Port conflict. Retrying ...')
                continue
            return _driver

    @log_printer('STOP server ...')
    def stop(self):
        """ 停止服务端 """
        # todo：杀不干净！
        if hasattr(self._server_process, 'appium_pid'):
            kill_process(self._server_process.appium_pid)
        self._server_process.terminate()
        self._driver.quit()

    def _get_driver(self, port_num):
        """ 获取driver对象 """
        self._driver = webdriver.Remote(
            'http://localhost:{}/wd/hub'.format(port_num),
            self.desired_caps)
        return self._driver