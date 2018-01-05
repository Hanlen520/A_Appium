from appium_client.appium_client import AppiumClient
from conf import DEVICE_CONF


# start
AppiumClient(DEVICE_CONF).run()
