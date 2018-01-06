from appium_client.appium_client import AppiumClient
from conf import DEVICE_LIST


TEST_SUITE = {
    '45O7E6TOSCF659LB': (
        'device1.app1.case1.Case1',
        'device1.app1.case2.Case2'
    )
}


if __name__ == '__main__':
    # start
    AppiumClient(DEVICE_LIST).run(TEST_SUITE)
