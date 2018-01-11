from .base_app1_api import BaseApp1API
from .page1.page1 import Page1
from .page2.page2 import Page2


class App1(object):
    def __init__(self):
        self.base_page = BaseApp1API()
        self.page1 = Page1()
        self.page2 = Page2()
