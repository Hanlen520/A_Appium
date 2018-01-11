from .base_app1_api import BaseApp1API
from .page1.page1 import Page1
from .page2.page2 import Page2


class App1(object):
    def __init__(self, _driver):
        self.base_page = BaseApp1API(_driver)
        self.page1 = Page1(_driver)
        self.page2 = Page2(_driver)
