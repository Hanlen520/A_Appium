import time
import os
import sys


# 判断系统类型，windows使用findstr，linux使用grep
system = sys.platform
if 'linux' in system:
    find_util = "grep"
else:
    find_util = "findstr"

# 判断是否设置环境变量ANDROID_HOME
if "ANDROID_HOME" in os.environ:
    if system == "Windows":
        command = os.path.join(
            os.environ["ANDROID_HOME"],
            "platform-tools",
            "adb.exe")
    else:
        command = os.path.join(
            os.environ["ANDROID_HOME"],
            "platform-tools",
            "adb")
else:
    if not os.path.exists(os.path.expanduser('~/SDK')):
        raise EnvironmentError(
            "Adb not found in $ANDROID_HOME path: %s." %
            os.environ["ANDROID_HOME"])
    else:
        command = os.path.join(
            os.path.expanduser('~/SDK'),
            "platform-tools",
            "adb")


class ADB(object):
    def __init__(self, device_id=None):
        if not device_id:
            self.device_id = ""
        else:
            self.device_id = "-s %s" % str(device_id)

    def adb(self, args):
        cmd = "%s %s %s" % (command, self.device_id, str(args))
        return os.system(cmd)

    def shell(self, args):
        cmd = "%s %s shell %s" % (command, self.device_id, str(args),)
        return os.system(cmd)

    def stay_wake(self):
        self.shell('settings put global stay_on_while_plugged_in 3')

    def screen_shot(self, appPath):
        """ 获取当前设备的截图,导出到指定目录 """
        self.shell("/system/bin/screencap -p /sdcard/temp.png")
        time.sleep(2)
        self.adb("pull /sdcard/temp.png %s" % appPath)