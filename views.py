from GbFramework import render
from main import application
from datetime import datetime
from models import TrainingSite
from custom_logging import Logger, debug

site = TrainingSite()
logger = Logger('views')


@application.add_route('/')
@debug
def course_list(request):
    logger.log('course_list')
    logger.log(f'categories = {site.categories}')
    logger.log(f'courses = {site.courses}')
    return '200 OK', render('course_list', courses=site.courses)


@application.add_route('/course-create/')
@debug
def course_create(request):
    if request['method'] == 'POST':
        logger.log('course_create POST')
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('interactive', name, category)
            site.courses.append(course)
        return '302 Moved Temporarily', render('course_list', courses=site.courses)
    else:
        logger.log('course_create GET')
        return '200 OK', render('course_create', categories=site.categories)


@application.add_route('/course-copy/')
@debug
def course_copy(request):
    logger.log('course_copy')
    params = request['params']
    name = params['name']
    old_course = site.get_course_by_name(name)
    if old_course:
        new_course = old_course.clone()
        site.courses.append(new_course)
    return '200 OK', render('course_list', courses=site.courses)


@application.add_route('/category-list/')
@debug
def category_list(request):
    logger.log('category_list')
    categories = site.find_parent_categories()
    logger.log(f'categories = {categories}')
    logger.log(f'courses = {site.courses}')
    return '200 OK', render('category_list', categories=categories)


@application.add_route('/category-create/')
@debug
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
        categories = site.find_parent_categories()
        return '302 Moved Temporarily', render('category_list', categories=categories)
    else:
        logger.log('category_create GET')
        categories = site.find_parent_categories()
        return '200 OK', render('category_create', categories=site.categories)


@application.add_route('/contact/')
@debug
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
