import os


class Device(object):
    def __init__(self, _device_id):
        # 设备的各项参数
        self.device_id = _device_id
        # 确认已连接
        self.is_connected()
        # 获取设备版本号
        self.system_version = self._get_device_conf('ro.build.version.sdk')
        self.device_name = self._get_device_conf('ro.product.name')

    def _get_device_conf(self, _conf_type):
        with os.popen(
            'adb -s {} shell cat /system/build.prop'.format(self.device_id)
        ) as device_info:
            lines = [each.strip('\n') for each in device_info.readlines()]
            for each_line in lines:
                if each_line.startswith('ro.') and '.{}'.format(_conf_type) in each_line:
                    return each_line.split('=')[1]

    def is_connected(self):
        with os.popen('adb devices') as device_list:
            for each_line in device_list.readlines():
                if self.device_id in each_line and 'device' in each_line:
                    return True
            else:
                raise ConnectionError('device {} not connected.'.format(self.device_id))

if __name__ == '__main__':
    Device('45O7E6TOSCF659LB').is_connected()