MODULE_TEMPLATE = '''
{dir_name}

Result
------


* Pass: {yes}
* Error: {no}
* Total: {total}

Error List
----------

{error_case}

Detail
------

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   :glob:

   cases*/result
'''


SECTION_TEMPLATE = '''
{case_name}

Time Usage
----------
{time} s


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

.. image:: screenshot.png

'''



from functools import wraps
from appium_client.appium_case import ReportObject
import os
def fix_report_object(func):
    @wraps(func)
    def call_it(_, _object):
        _result = ReportObject(
            case_name = _object.case_name if _object.case_name else 'Default case',
            status = _object.status,
            traceback = _object.traceback if _object.traceback else '',
            screenshot = _object.screenshot if _object.screenshot else '',
            time_cost = _object.time_cost
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
        # 正确/错误 用例的列表
        self.pass_list = list()
        self.error_list = list()

    @fix_report_object
    def add_section(self, _report_object):
        """ 增加条目 """
        if _report_object.status:
            _template = SECTION_TEMPLATE
            self.pass_list.append(_report_object)
        else:
            _template = SECTION_TEMPLATE + ERROR_TEMPLATE
            self.error_list.append(_report_object)

        ori_case_name = _report_object.case_name.split(os.sep)[-1]
        case_name = ori_case_name + '\n' + '='*len(ori_case_name)

        status = 'OK' if _report_object.status else 'ERROR'
        if status == 'OK':
            status = '**{}**'.format(status)
        else:
            status = '*{}*'.format(status)

        traceback_str = ('\n' + _report_object.traceback).replace('\n', '\n'+' '*4)
        time_cost = _report_object.time_cost

        html_content = _template.format(
            case_name=case_name,
            status=status,
            screenshot=ori_case_name,
            traceback=traceback_str,
            time=time_cost
        )

        _case_result_path = os.path.join(self._dir_path, ori_case_name, 'result.rst')
        with open(_case_result_path, 'w+') as f:
            f.write(html_content)

        self._content.append(os.path.join(ori_case_name, 'result'))

    def build(self):
        """ 构建报告 """
        with open(self._output_path, 'w+') as _result_file:
            # title
            _dir_path = self._dir_path.split(os.sep)[-1]
            _dir_path = '{}\n{}'.format(_dir_path, len(_dir_path)*'=')
            # data analysis
            _pass_case_num = len(self.pass_list)
            _error_case_num = len(self.error_list)
            _total_num = _pass_case_num + _error_case_num
            _error_case_list = ''.join(['* {}'.format(each.case_name) for each in self.error_list])
            # write in
            _content = MODULE_TEMPLATE.format(
                dir_name=_dir_path,
                yes=_pass_case_num,
                no=_error_case_num,
                total=_total_num,
                error_case=_error_case_list,
            )
            _result_file.write(_content)
