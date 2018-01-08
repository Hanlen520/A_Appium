from appium_client.appium_client import AppiumClient
from conf import DEVICE_LIST
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

TEST_SUITE = {
    '45O7E6TOSCF659LB': (
        'cases.device1.app1.case1.Case1',
        'cases.device1.app1.case2.Case2'
    )
}

if __name__ == '__main__':
    # start
    AppiumClient(DEVICE_LIST).run(TEST_SUITE)
