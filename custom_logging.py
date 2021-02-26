from GbFramework import SingletonByName
from datetime import datetime


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    def log(self, text):
        dt_string = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f'{dt_string} - [{self.name}] - {text}')