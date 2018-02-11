# 一个最最简单的使用appium client进行操作的例子
from appium_client.appium import webdriver
import subprocess


# a simple example

# build desired caps
desired_caps = {}
desired_caps['deviceName'] = '45O7E6TOSCF659LB-TP908A'
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = 25
desired_caps['appPackage'] = 'com.cyanogenmod.trebuchet'
desired_caps['appActivity'] ='com.android.launcher3.Launcher'
desired_caps['dontStopAppOnReset'] = True
desired_caps['noReset'] = True
desired_caps['stopAppAtEnd'] = False
desired_caps['autoUnlock'] = False
desired_caps['newCommandTimeout'] = 600

# start server
server_cmd = ' appium -p 26270 -bp 27235 -U 45O7E6TOSCF659LB --local-timezone  --command-timeout 1200 --log-timestamp  --session-override '
server = subprocess.Popen(server_cmd, shell=True)

# init driver
driver = webdriver.Remote('http://localhost:26270/wd/hub', desired_caps)

# do something
driver.swipe(100,100, 200,200, 500)

# after all
driver.quit()
server.kill()