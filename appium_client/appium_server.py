import subprocess
from .appium import webdriver
from .console_utils import log_printer, logi, kill_process
from conf import ANDROID_HOME, JAVA_HOME, APPIUM_HOME
import random
import sys
import os
import time

# 端口范围
PORT_LIST = list(range(25000, 26000))
BOOTSTRAP_PORT_LIST = list(range(26001, 27000))

# 环境配置
START_TIME_LIMIT = 200
if 'linux' in sys.platform:
    ENV_STR = '''
    export ANDROID_HOME=%s
    export JAVA_HOME=%s
    export NODE_HOME=%s
    export PATH=$JAVA_HOME/bin:$ANROID_HOME:$NODE_HOME:$PATH

    ''' % (ANDROID_HOME, JAVA_HOME, APPIUM_HOME)
else:
    ENV_STR = ''

SERVER_COMMAND = ENV_STR + ' appium -p {port} -bp {bootstrap_port} -U {device_id} --local-timezone  --command-timeout 1200 --log-timestamp  --session-override '


def _is_port_using(_port_num):
    """ 端口是否被使用 """
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
    def __init__(self, _arg_dict):
        #
        self.desired_caps = self._get_desire_caps(_arg_dict)
        # 服务端子进程对象
        self._server_process = None
        # 对应的driver
        self._driver = None

    def _get_desire_caps(self, _arg_dict):
        """ 获取配置 """
        _desired_caps = dict()
        _desired_caps['deviceName'] = '{}-{}'.format(
            _arg_dict['device_id'], _arg_dict['device_name']
        )
        _desired_caps['platformName'] = 'Android'
        _desired_caps['platformVersion'] = _arg_dict['system_version']
        _desired_caps['appPackage'] = _arg_dict['app_package']
        _desired_caps['appActivity'] = _arg_dict['app_activity']
        _desired_caps['dontStopAppOnReset'] = True
        _desired_caps['noReset'] = True
        _desired_caps['stopAppAtEnd'] = False
        _desired_caps['autoUnlock'] = True
        _desired_caps['newCommandTimeout'] = 600

        return _desired_caps

    @log_printer('start server')
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
                time.sleep(8)
                _driver = self._get_driver(port_num)
            else:
                logi('Port conflict. Retrying ...')
                continue
            return _driver

    @log_printer('stop server')
    def stop(self):
        """ 停止服务端 """
        # todo：杀不干净！
        self._driver.quit()
        if hasattr(self._server_process, 'pid'):
            kill_process(self._server_process.pid)
        self._server_process.terminate()
        self._server_process = None

    def _get_driver(self, port_num):
        """ 获取driver对象 """
        self._driver = webdriver.Remote(
            'http://localhost:{}/wd/hub'.format(port_num),
            self.desired_caps)
        return self._driver