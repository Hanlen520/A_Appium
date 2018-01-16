"""
所有api的基类
"""


class BaseAPI(object):
    def __init__(self, _driver):
        self.driver = _driver