from GbFramework import render
from datetime import datetime

def index_view(request):
    return '200 OK', render('index')


def secret_view(request):
    secret_key = request.get('secret_key', None)
    return '200 OK', render('secret', secret_key=secret_key)

def contact_view(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        email = data['email']
        subject = data['subject']
        message = data['message']

        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} === Пришло сообщение ===\n')
            f.write(f'От кого: {name} ({email})\n')
            f.write(f'Тема: {subject}\n')
            f.write(f'Тело: {message}\n')

    return '200 OK', render('contact')