from functools import wraps
import logging
import datetime
logging.basicConfig(level=logging.DEBUG)

def log_printer(_message):
    def m_decorator(func):
        @wraps(func)
        def call_it(*args, **kwargs):
            logging.info('{} begin in {}'.format(_message, _get_now()))
            _result = func(*args, **kwargs)
            logging.info('{} done in {}.'.format(_message, _get_now()))
            return _result
        return call_it
    return m_decorator

def _get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
