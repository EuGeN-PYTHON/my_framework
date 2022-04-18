import copy
import quopri


class User:
    pass


class Worker(User):
    pass


class Client(User):
    pass


class UserFactory:
    types = {
        'worker': Worker,
        'client': Client
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class ObjectPrototype:

    def clone(self):
        return copy.deepcopy(self)


class Object(ObjectPrototype):

    # инициализация объекта при создании
    def __init__(self,  typeobject, name=None, vk_num=None, t2_num=None, mf_num=None, mt_num=None):
        self.name = name
        self.vk_num = vk_num
        self.t2_num = t2_num
        self.mf_num = mf_num
        self.mt_num = mt_num
        self.typeobject = typeobject
        self.typeobject.objects.append(self)


# Объект конструктива опора/столб
class PillarObject(Object):
    pass


# Объект конструктива мачта
class TowerObject(Object):
    pass


# Категория
class TypeObject:
    # реестр?
    auto_id = 0

    def __init__(self, name, typeobject):
        self.id = TypeObject.auto_id
        TypeObject.auto_id += 1
        self.name = name
        self.typeobject = typeobject
        self.objects = []

    def objects_count(self):
        result = len(self.objects)
        if self.typeobject:
            result += self.typeobject.objects_count()
        return result


# порождающий паттерн Абстрактная фабрика - фабрика объектов
class ObjectFactory:
    types = {
        'pillar': PillarObject,
        'tower': TowerObject
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.workers = []
        self.clients = []
        self.objects = []
        self.typeobject = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_type(name, typeobject=None):
        return TypeObject(name, typeobject)

    def find_type_by_id(self, id):
        for item in self.typeobject:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет типа объекта с id = {id}')

    @staticmethod
    def create_object(type_, name, typeobject):
        return ObjectFactory.create(type_, name, typeobject)

    def get_object(self, name):
        for item in self.objects:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
