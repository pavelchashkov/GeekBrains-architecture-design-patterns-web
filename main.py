from GbFramework import WebApp
from views import index_view, secret_view


def fc_add_secret_key(request):
    request['secret_key'] = 'SECRET_KEY'

front_controllers = [
    fc_add_secret_key
]

routes = {
    '/': index_view,
    '/secret/': secret_view,
}

application = WebApp(routes, front_controllers)
