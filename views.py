from GbFramework.templates import render
from GbFramework.orm import UnitOfWork
from GbFramework.templates.cbv import ListView, CreateView
from main import application
from datetime import datetime
from models import TrainingSite, SmsNotifier, EmailNotifier
from custom_logging import Logger, debug, FileWriter
from serializers import BaseSerializer
from models_mappers import MapperRegistry

site = TrainingSite()
logger = Logger('views', writer=FileWriter('app.log'))
sms_notifier = SmsNotifier()
email_notifier = EmailNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


class CourseListView(ListView):
    template_name = 'course_list'
    queryset = site.courses


class CourseCreateView(CreateView):
    template_name = 'course_create'

    def get_context_data(self):
        return {'categories': site.categories}

    def render_post(self, request):
        return CourseListView()(request)

    def create_obj(self, data):
        name = data['name']
        category_id = data.get('category_id')
        if category_id:
            category = site.get_category_by_id(int(category_id))
            course = site.create_course('interactive', name, category)
            course.observers.append(sms_notifier)
            course.observers.append(email_notifier)
            site.courses.append(course)


class CategoryListView(ListView):
    template_name = 'category_list'

    def get_queryset(self):
        return site.find_parent_categories()


class CategoryCreateView(CreateView):
    template_name = 'category_create'

    def get_context_data(self) -> dict:
        return {'categories': site.categories}

    def create_obj(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')
        category = site.get_category_by_id(
            int(category_id)) if category_id else None
        new_category = site.create_category(name, category)
        site.categories.append(new_category)

    def render_post(self, request):
        return CategoryListView()(request)


class UserListView(ListView):
    template_name = 'user_list'
    # queryset = site.users

    def get_queryset(self):
          return MapperRegistry.get_current_mapper('student').all()

class UserCreateView(CreateView):
    template_name = 'user_create'

    def render_post(self, request):
        return UserListView()(request)

    def create_obj(self, data: dict):
        name = data['name']
        user = site.create_user('student', name)
        site.users.append(user)
        user.mark_new()
        UnitOfWork.get_current().commit()


@application.add_route('/course-create/')
@debug
def course_create(request):
    return CourseCreateView()(request)


@application.add_route('/course-copy/')
@debug
def course_copy(request):
    logger.log('course_copy')
    params = request['params']
    name = params['name']
    old_course = site.find_course_by_name(name)
    if old_course:
        new_course = old_course.clone()
        site.courses.append(new_course)
    return CourseListView()(request)


@application.add_route('/category-list/')
@debug
def category_list(request):
    return CategoryListView()(request)


@application.add_route('/category-create/')
@debug
def category_create(request):
    return CategoryCreateView()(request)


@application.add_route('/user-list/')
@debug
def user_list(request):
    return UserListView()(request)


@application.add_route('/user-create/')
@debug
def user_create(request):
    return UserCreateView()(request)


@application.add_route('/api/courses/')
@debug
def api_courses(request):
    return '200 OK', BaseSerializer(site.courses).save()


@application.add_route('/')
@debug
def course_list(request):
    return CourseListView()(request)


@application.add_route('/add-user-on-course/')
@debug
def add_user_on_course(request):
    logger.log(f"add-user-on-course {request['method']}")
    if request['method'] == 'POST':
        data = request['data']
        user_id = int(data['user_id'])
        course_id = int(data['course_id'])
        user = site.get_user_by_id(user_id)
        course = site.get_course_by_id(course_id)
        course.add_user(user)
        return CourseListView()(request)
    else:
        return '200 OK', render('add_user_on_course', users=site.users, courses=site.courses)


@application.add_route('/contact/')
@debug
def contact_view(request):
    logger.log(f"contact_view {request['method']}")
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
