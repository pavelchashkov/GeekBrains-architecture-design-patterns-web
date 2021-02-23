class User:
    pass


class Player(User):
    pass


class Organizer(User):
    pass


class UserFactory:
    types = {
        'player': Player,
        'organizer': Organizer,
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Category:

    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        self.name = name
        self.category = category
        Category.auto_id += 1
        self.tournaments = []

    def tournament_count(self):
        result = len(self.tournaments)
        if self.category:
            result += self.category.tournament_count()
        return result


class Tournament:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.tournaments.append(self)


class IndividualTournament(Tournament):
    pass


class CommandTournament(Tournament):
    pass


class TournamentFactory:
    types = {
        'individual': IndividualTournament,
        'command': CommandTournament,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class CompMapSite:
    def __init__(self):
        self.players = []
        self.organizers = []
        self.tournaments = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_tournament(type_, name, category) -> None:
        return TournamentFactory.create(type_, name, category)

    def get_tournament_by_name(self, name) -> Tournament:
        for item in self.tournaments:
            if item.name == name:
                return item
        return None
