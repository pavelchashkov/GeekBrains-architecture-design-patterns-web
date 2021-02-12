from GbFramework import render

def index_view(request):
    return '200 OK', render('index')


def secret_view(request):
    secret_key = request.get('secret_key', None)
    return '200 OK', render('secret', secret_key=secret_key)