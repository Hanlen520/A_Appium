import subprocess
from .appium import webdriver


SERVER_COMMAND = ' appium -p {port} -bp {bootstrap_port} -U {device_id} --local-timezone  --command-timeout 1200 --log-timestamp  --session-override '


class AppiumServer(object):
    def __init__(self, _device):
        # 设备对象
        self.device = _device
        #
        self.desired_caps = None
        # 服务端子进程对象
        self._server_process = None

    @staticmethod
    def _get_desire_caps(_device):
        # TODO: 在device里添加各项参数
        _desired_caps = dict()
        _desired_caps['deviceName'] = '{}-TP908A'.format(_device.device_id)
        _desired_caps['platformName'] = 'Android'
        _desired_caps['platformVersion'] = 25
        _desired_caps['appPackage'] = 'com.cyanogenmod.trebuchet'
        _desired_caps['appActivity'] = 'com.android.launcher3.Launcher'
        _desired_caps['dontStopAppOnReset'] = True
        _desired_caps['noReset'] = True
        _desired_caps['stopAppAtEnd'] = False
        _desired_caps['autoUnlock'] = False
        _desired_caps['newCommandTimeout'] = 600

        return _desired_caps

    def start(self):
        self.desired_caps = self._get_desire_caps(self.device)

        _cmd = SERVER_COMMAND.format(
            # todo: auto calculate these ports num
            port = 26270,
            bootstrap_port = 27235,
            device_id = self.desired_caps['deviceName'].split('-')[0]
        )
        self._server_process = subprocess.Popen(_cmd, shell=True)
        return self._get_driver()

    def stop(self):
        self._server_process.terminate()

    def _get_driver(self):
        # TODO: port num
        return webdriver.Remote('http://localhost:26270/wd/hub', self.desired_caps)
