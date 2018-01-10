from ..base_device_api import BaseDeviceAPI
from .page1.page1 import Page1
from .page2.page2 import Page2


class App1(BaseDeviceAPI):
    def __init__(self, *args, **kwargs):
        super(App1, self).__init__(*args, **kwargs)

        self.page1 = Page1()
        self.page2 = Page2()
