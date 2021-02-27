from resource.prototypes import PrototypeMixin
from custom_logging import Logger

logger = Logger('models')


class User:
    def __init__(self, name):
        self.name = name


class Student(User):
    pass


class Teacher(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Category:

    auto_id = 0

    def __init__(self, name, parent_category):
        self.id = Category.auto_id
        self.name = name
        self.children = []
        self.courses = []
        self.have_parent = False
        Category.auto_id += 1
        if parent_category:
            self.have_parent = True
            parent_category.children.append(self)
        logger.log(self)

    def course_count(self):
        logger.log('Calc course_count')
        result = len(self.courses)
        if len(self.children) > 0:
            for item in self.children:
                result += item.course_count()
        logger.log(result)
        return result

    @property
    def member(self):
        return "child" if self.have_parent else "parent"

    def __repr__(self):
        return f'<{self.__class__.__name__}> "{self.name}" ({self.member})'

    def __str__(self):
        return self.__repr__()


class Course(PrototypeMixin):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

    def clone(self):
        copy_object = super().clone()
        copy_object.name += '_copy'
        copy_object.category = self.category
        copy_object.category.courses.append(copy_object)
        return copy_object


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingSite:
    def __init__(self):
        self.users = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_parent_categories(self):
        return [c for c in self.categories if not c.have_parent]

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category) -> None:
        return CourseFactory.create(type_, name, category)

    def get_course_by_name(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None
