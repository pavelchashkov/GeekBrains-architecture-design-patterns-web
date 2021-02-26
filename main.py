from wsgiref.simple_server import make_server
from GbFramework import WebApp
from importlib import import_module
from custom_logging import Logger

logger = Logger('main')


def fc_add_secret_key(request):
    request['secret_key'] = 'SECRET_KEY'


front_controllers = [
    fc_add_secret_key
]

application = WebApp('MyApp', front_controllers)
import_module('views')

if __name__ == '__main__':
    print(application)
    with make_server('localhost', 8000, application) as httpd:
        logger.log('Start test web server on port 8000')
        httpd.serve_forever()
