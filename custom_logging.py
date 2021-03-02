from GbFramework import SingletonByName
from datetime import datetime


class ConsoleWriter:
    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self, file_name) -> None:
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        dt_string = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log_text = f'{dt_string} - [{self.name}] - {text}'
        self.writer.write(log_text)


def debug(func):
    def inner(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        duration = (end - start).total_seconds()
        fmt_start = start.strftime("%Y-%m-%d %H:%M:%S")
        fmt_end = end.strftime("%Y-%m-%d %H:%M:%S")
        print(
            f'DEBUG - func: {func.__name__} - duration: {duration:.3} | start_time: {fmt_start} | end_time: {fmt_end}')
        return result
    return inner
