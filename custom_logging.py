from GbFramework import SingletonByName
from datetime import datetime


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        dt_string = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f'{dt_string} - [{self.name}] - {text}')


def debug(func):
    def inner(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        duration = (end - start).total_seconds()
        fmt_start = start.strftime("%Y-%m-%d %H:%M:%S")
        fmt_end = end.strftime("%Y-%m-%d %H:%M:%S")
        print(f'DEBUG - func: {func.__name__} - duration: {duration:.3} | start_time: {fmt_start} | end_time: {fmt_end}')
        return result
    return inner
