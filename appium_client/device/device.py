class Device(object):
    def __init__(self, _device_conf):
        # 设备的各项参数
        self.device_id = None

        # 贴参数
        self._parse_conf(_device_conf)

    def _parse_conf(self, _conf):
        # 应用各项设置
        self.device_id = _conf['device_id']