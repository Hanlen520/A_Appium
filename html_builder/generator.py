import os
import shutil
from appium_client.console_utils import log_printer


GENERATOR_DIR = os.path.join(os.getcwd(), 'html_builder')
SOURCE_DIR = os.path.join(GENERATOR_DIR, 'source', 'report_source')


@log_printer('load result files')
def load_result(_ori_dir, _target_dir):
    _target_dir_list = os.listdir(_target_dir)
    for each in os.listdir(_ori_dir):
        if each.startswith('RESULT') and each not in _target_dir_list:
            _src = os.path.join(_ori_dir, each)
            _des = os.path.join(SOURCE_DIR, each)
            if os.path.exists(_des):
                shutil.rmtree(_des)
            shutil.copytree(_src, _des)


class Generator(object):
    def __init__(self, _result_dir):
        self.result_dir = _result_dir
        load_result(self.result_dir, SOURCE_DIR)

    @log_printer('build html report')
    def build(self):
        os.chdir(GENERATOR_DIR)
        os.system('make html')
        os.chdir(os.getcwd())
