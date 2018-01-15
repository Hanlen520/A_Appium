MODULE_TEMPLATE = '''
CASES REPORT
============

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   :glob:

   cases*/result
'''


SECTION_TEMPLATE = '''
{case_name}


Test Result
-----------

{status}

'''

ERROR_TEMPLATE = '''
Traceback
---------

::

{traceback}

ScreenShot
----------

.. image:: {case_name}/screenshot.png

'''



from functools import wraps
from appium_client.appium_case import ReportObject
import os
def fix_report_object(func):
    @wraps(func)
    def call_it(_, _object):
        _result = ReportObject(
            case_name = _object.case_name if _object.case_name else 'Default case',
            status = _object.status if _object.status else True,
            traceback = _object.traceback if _object.traceback else '',
            screenshot = _object.screenshot if _object.screenshot else ''
        )
        return func(_, _result)
    return call_it


class ReportGenerator(object):
    def __init__(self, _output_path):
        # 入口rst文件位置
        self._output_path = _output_path
        # 根目录位置
        self._dir_path = os.path.dirname(self._output_path)
        self._content = list()

    @fix_report_object
    def add_section(self, _report_object):
        """ 增加条目 """
        if _report_object.status:
            _template = SECTION_TEMPLATE
        else:
            _template = SECTION_TEMPLATE + ERROR_TEMPLATE

        ori_case_name = _report_object.case_name
        case_name = ori_case_name + '\n' + '='*len(ori_case_name)

        status = 'OK' if _report_object.status else 'ERROR'
        status = '**{}**'.format(status)

        traceback_str = ('\n' + _report_object.traceback).replace('\n', '\n'+' '*4)
        screen_path = _report_object.screenshot

        html_content = _template.format(
            case_name=case_name,
            status=status,
            screenshot=screen_path,
            traceback=traceback_str,
        )

        _case_result_path = os.path.join(self._dir_path, ori_case_name, 'result.rst')
        with open(_case_result_path, 'w+') as f:
            f.write(html_content)

        self._content.append(os.path.join(ori_case_name, 'result'))

    def build(self):
        """ 构建报告 """
        with open(self._output_path, 'w+') as _result_file:
            _result_file.write(MODULE_TEMPLATE)
