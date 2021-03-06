import sqlite3
from models import Student, Category, Course

connection = sqlite3.connect('app.sqlite')


class BaseMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def select_all_raw_data(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def select_by_id_raw_data(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundException(f'Record with id={id} not found')

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def sql_commit_raw_data(self, statement, params):
        self.cursor.execute(statement, params)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)


class StudentMapper(BaseMapper):
    tablename = 'student'

    def all(self):
        result = []
        for item in self.select_all_raw_data():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        result = self.select_by_id_raw_data(id)
        return Student(*result)

    def insert(self, obj):
        self.sql_commit_raw_data(
            f"INSERT INTO {self.tablename} (name) VALUES (?)", 
            (obj.name,)
        )

    def update(self, obj):
        self.sql_commit_raw_data(
            f"UPDATE {self.tablename} SET name=? WHERE id=?",
            (obj.name, obj.id)
        )
        

class CategoryMapper(BaseMapper):
    tablename = 'category'

    def all(self):
        result = []
        for item in self.select_all_raw_data():
            id, name = item
            category = Category(name)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        result = self.select_by_id_raw_data(id)
        return Category(*result)

    def insert(self, obj):
        self.sql_commit_raw_data(
            f"INSERT INTO {self.tablename} (name) VALUES (?)", 
            (obj.name,)
        )

    def update(self, obj):
        self.sql_commit_raw_data(
            f"UPDATE {self.tablename} SET name=? WHERE id=?",
            (obj.name, obj.id)
        )

class CourseMapper(BaseMapper):
    tablename = 'course'

    def all(self):
        result = []
        for item in self.select_all_raw_data():
            id, name = item
            course = Course(name)
            course.id = id
            result.append(course)
        return result

    def find_by_id(self, id):
        result = self.select_by_id_raw_data(id)
        return Course(*result)

    def insert(self, obj):
        self.sql_commit_raw_data(
            f"INSERT INTO {self.tablename} (name) VALUES (?)", 
            (obj.name,)
        )

    def update(self, obj):
        self.sql_commit_raw_data(
            f"UPDATE {self.tablename} SET name=? WHERE id=?",
            (obj.name, obj.id)
        )


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        if isinstance(obj, Course):
            return CourseMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')
