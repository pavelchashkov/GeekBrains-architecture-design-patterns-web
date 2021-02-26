from GbFramework import render
from main import application
from datetime import datetime
from models import CompMapSite
from custom_logging import Logger

site = CompMapSite()
logger = Logger('views')


@application.add_route('/')
def tournament_list(request):
    logger.log('tournament_list')
    logger.log(f'categories = {site.categories}')
    logger.log(f'tournaments = {site.tournaments}')
    return '200 OK', render('tournament_list', tournaments=site.tournaments)


@application.add_route('/tournament-create/')
def tournament_create(request):
    if request['method'] == 'POST':
        logger.log('tournament_create POST')
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        if category_id:
            category = site.find_category_by_id(int(category_id))
            tournament = site.create_tournament('individual', name, category)
            site.tournaments.append(tournament)
        return '302 Moved Temporarily', render('tournament_list', tournaments=site.tournaments)
    else:
        logger.log('tournament_create GET')
        return '200 OK', render('tournament_create', categories=site.categories)


@application.add_route('/tournament-copy/')
def tournament_copy(request):
    logger.log('tournament_copy')
    params = request['params']
    name = params['name']
    old_tournament = site.get_tournament_by_name(name)
    if old_tournament:
        new_tournament = old_tournament.clone()
        new_tournament.name = f'{name}_copy'
        site.tournaments.append(new_tournament)
    return '200 OK', render('tournament_list', tournaments=site.tournaments)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('category_list')
    logger.log(f'categories = {site.categories}')
    logger.log(f'tournaments = {site.tournaments}')
    return '200 OK', render('category_list', categories=site.categories)


@application.add_route('/category-create/')
def category_create(request):
    if request['method'] == 'POST':
        logger.log('category_create POST')
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = site.find_category_by_id(
            int(category_id)) if category_id else None
        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        return '302 Moved Temporarily', render('category_list', categories=site.categories)
    else:
        logger.log('category_create GET')
        return '200 OK', render('category_create', categories=site.categories)

@application.add_route('/contact/')
def contact_view(request):
    if request['method'] == 'POST':
        logger.log('contact_view POST')
        data = request['data']
        name = data['name']
        email = data['email']
        subject = data['subject']
        message = data['message']

        with open('messages.txt', 'a', encoding='utf-8') as f:
            f.write(
                f'\n{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} === Пришло сообщение ===\n')
            f.write(f'От кого: {name} ({email})\n')
            f.write(f'Тема: {subject}\n')
            f.write(f'Тело: {message}\n')

    return '200 OK', render('contact')
