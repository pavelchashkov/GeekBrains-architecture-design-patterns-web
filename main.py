from GbFramework import WebApp
from views import tournament_list, tournament_create, category_list, tournament_copy, category_create, contact_view


def fc_add_secret_key(request):
    request['secret_key'] = 'SECRET_KEY'


front_controllers = [
    fc_add_secret_key
]

routes = {
    '/': tournament_list,
    '/tournament-create/': tournament_create,
    '/tournament-copy/': tournament_copy,
    '/category-list/': category_list,
    '/category-create/': category_create,
    '/contact/': contact_view,
}

application = WebApp(routes, front_controllers)
