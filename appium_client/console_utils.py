from functools import wraps
import logging
import datetime
import os
import sys
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s:%(levelname)s %(message)s'
)
logi = logging.info

def log_printer(_message):
    def m_decorator(func):
        @wraps(func)
        def call_it(*args, **kwargs):
            logging.info(_message)
            _result = func(*args, **kwargs)
            # logging.info('{} done in {}.'.format(_message, _get_now()))
            return _result
        return call_it
    return m_decorator

def _get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def kill_process(_pid):
    _pid_cmd = 'kill -9 {}' if 'linux' in sys.platform else 'taskkill /F /pid {}'
    os.system(_pid_cmd.format(_pid))


