import markdown


CSS_TEMPLATE = '''
<style type="text/css">
h1 {background-color: {COLOR}}
</style>
'''

TEMPLATE = '''
# {case_name}

# {status}

![]({screenshot})

{traceback}

'''

STATUS_DICT = {
    'OK': 'green',
    'ERROR': 'red'
}


def markdown2html(report_object, target_path):
    case_name = report_object.case_name
    status = 'OK' if report_object.status else 'ERROR'
    traceback_str = report_object.traceback
    screen_path = report_object.screenshot

    html_content = CSS_TEMPLATE.replace('{COLOR}', STATUS_DICT[status])
    html_content += markdown.markdown(
        TEMPLATE.format(
            case_name=case_name,
            status=status,
            screenshot=screen_path,
            traceback=traceback_str,
            css=STATUS_DICT[status]
        )
    )

    with open(target_path, 'w+') as _html:
        _html.write(html_content)


if __name__ == '__main__':
    from collections import namedtuple
    ReportObject = namedtuple('ReportObject', ['case_name', 'status', 'traceback', 'screenshot'])
    markdown2html(ReportObject('hello', True, 'aldskfjalkdjbvz,mcxnbvz,mncv', 'nothing'), 'test_for_test.html')