import markdown


SECTION_TEMPLATE = '''
# {case_name}

## {status}

![]({screenshot})

{traceback}

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


class ReportGenerator(object):
    def __init__(self):
        # markdown 内容
        self._content = str()
        self._head = CSS_TEMPLATE.replace('{COLOR}', STATUS_DICT['OK'])

    def add_section(self, _report_object):
        case_name = _report_object.case_name
        status = 'OK' if _report_object.status else 'ERROR'
        traceback_str = ('\n' + _report_object.traceback).replace('\n', '\n'+' '*8)
        screen_path = _report_object.screenshot

        html_content = SECTION_TEMPLATE.format(
            case_name=case_name,
            status=status,
            screenshot=screen_path,
            traceback=traceback_str,
        )

        self._content += html_content

    def build(self):
        return self._content
        # return markdown.markdown(self._head + self._content)


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