SECTION_TEMPLATE = '''
{case_name}


Test Result
-----------

{status}


Traceback
---------

::

{traceback}


ScreenShot
----------

.. image:: {case_name}/screenshot.png

'''


CSS_TEMPLATE = '''
<style type="text/css">
h1 {background-color: {COLOR}}
</style>
'''

STATUS_DICT = {
    'OK': 'green',
    'ERROR': 'red'
}


from functools import wraps
from appium_client.appium_case import ReportObject
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
        # markdown 内容
        self._output_path = _output_path
        self._content = str()
        self._head = CSS_TEMPLATE.replace('{COLOR}', STATUS_DICT['OK'])

    @fix_report_object
    def add_section(self, _report_object):
        """ 增加条目 """
        case_name = _report_object.case_name
        case_name += '\n' + '='*len(case_name)

        status = 'OK' if _report_object.status else 'ERROR'
        status += '\n' + '-'*len(status)

        traceback_str = ('\n' + _report_object.traceback).replace('\n', '\n'+' '*4)
        screen_path = _report_object.screenshot

        html_content = SECTION_TEMPLATE.format(
            case_name=case_name,
            status=status,
            screenshot=screen_path,
            traceback=traceback_str,
        )

        self._content += html_content

    def build(self):
        """ 构建报告 """
        with open(self._output_path, 'w+') as _result_file:
            _result_file.write(self._content)


if __name__ == '__main__':
    from collections import namedtuple
    ReportObject = namedtuple('ReportObject', ['case_name', 'status', 'traceback', 'screenshot'])
    report_g = ReportGenerator()
    report_g.add_section(
        ReportObject(
            'case111111', True,
            'alkdsjhfalkjsdhfaljkfd', 'aa.png'
        )
    )
    report_g.add_section(
        ReportObject(
            'case1222222', True,
            'alkdsjhfal\nkjsdhfaljkfd', 'aa.png'
        )
    )
    report_g.add_section(
        ReportObject(
            'case333333331', False,
            'alkdsjhfal\nkjsdhfaljkfd', 'aa.png'
        )
    )
    print(report_g.build())