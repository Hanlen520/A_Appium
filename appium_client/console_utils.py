from functools import wraps
import logging
import datetime
import os
import sys
import time
import importlib

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s:%(levelname)s %(message)s'
)
logi = logging.info


def log_printer(_message):
    def m_decorator(func):
        @wraps(func)
        def call_it(*args, **kwargs):
            logi(_message)
            _result = func(*args, **kwargs)
            logi('End {}'.format(_message))
            return _result
        return call_it
    return m_decorator


def _get_now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def timer(func):
    @wraps(func)
    def call_it(*arg, **kwargs):
        _start_time = time.time()
        _result = func(*arg, **kwargs)
        _time_used = round(time.time() - _start_time, 3)
        logi('Time usage: {}s'.format(_time_used))
        return _result
    return call_it


def kill_process(_pid):
    """ 根据进程id杀死进程 """
    _pid_cmd = 'kill -9 {}' if 'linux' in sys.platform else 'taskkill /pid {} /F'
    os.system(_pid_cmd.format(_pid))


def import_class(import_str):
    """ Returns a class from a string including module and class. """
    mod_str, _sep, class_str = import_str.rpartition('.')
    _module = importlib.import_module(mod_str)
    return getattr(_module, class_str)


