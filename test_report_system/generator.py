import os
import shutil


GENERATOR_DIR = os.path.join(os.getcwd(), 'test_report_system')
SOURCE_DIR = os.path.join(GENERATOR_DIR, 'source', 'report_source')


def load_result(_ori_dir, _target_dir):
    _target_dir_list = os.listdir(_target_dir)
    for each in os.listdir(_ori_dir):
        if each.startswith('RESULT') and each not in _target_dir_list:
            shutil.copytree(each, SOURCE_DIR)


class Generator(object):
    def __init__(self, _result_dir):
        self.result_dir = _result_dir
        load_result(self.result_dir, SOURCE_DIR)

    def build(self):
        os.chdir(GENERATOR_DIR)
        os.system('make html')
        os.chdir(os.getcwd())
