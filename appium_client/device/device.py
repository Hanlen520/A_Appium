import os
from .adb import ADB
from ..console_utils import logi
from appium_client.appium_server import AppiumServer


DEVICE_LIST = dict()


class Device(object):
    def __init__(self, _device_id):
        # 设备的各项参数
        self.device_id = _device_id
        # 确认已连接
        self._is_connected()
        # 获取设备版本号
        self.system_version = self._get_device_conf('ro.build.version.sdk')
        self.device_name = self._get_device_conf('ro.product.name')
        # adb
        self.adb = ADB(self.device_id)
        self.adb.stay_wake()
        # 当前测试的app
        self.cur_app = None
        # 对应的server与driver
        self.server = None
        self.driver = None

    def __str__(self):
        return '{} - {}'.format(self.device_name, self.device_id)

    def __repr__(self):
        return self.__str__()

    def bind(self, _case_object):
        if self.cur_app == _case_object.app_name:
            return None
        else:
            self.stop()
            self.cur_app = _case_object.app_name

        _server_dict = {
            'device_id': self.device_id,
            'device_name': self.device_name,
            'system_version': self.system_version,
            'app_package': _case_object.module_object.app_package,
            'app_activity': _case_object.module_object.app_activity
        }

        self.server = AppiumServer(_server_dict)
        self.driver = self.server.start()

    def stop(self):
        try:
            self.server.stop()
        except:
            pass
        self.driver = None
        self.server = None

    def _get_device_conf(self, _conf_type):
        with os.popen(
            'adb -s {} shell cat /system/build.prop'.format(self.device_id)
        ) as device_info:
            lines = [each.strip('\n') for each in device_info.readlines()]
            for each_line in lines:
                if each_line.startswith('ro.') and _conf_type in each_line:
                    return each_line.split('=')[1]

    def _is_connected(self):
        with os.popen('adb devices') as device_list:
            for each_line in device_list.readlines():
                if self.device_id in each_line and 'device' in each_line:
                    return True
            else:
                raise ConnectionError('device {} not connected.'.format(self.device_id))

    def get_screen_shot(self, _path):
        self.adb.screen_shot(_path)

if __name__ == '__main__':
    Device('45O7E6TOSCF659LB')._is_connected()