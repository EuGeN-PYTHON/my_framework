import threading


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.change_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_update(self, obj):
        self.change_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_objects()
        self.delete_objects()

        self.new_objects.clear()
        self.change_objects.clear()
        self.removed_objects.clear()

    def insert_new(self):
        print(self.new_objects)
        for obj in self.new_objects:
            print(f"Вывожу {self.MapperRegistry}")
            self.MapperRegistry.get_mapper(obj).insert(obj)

    def update_objects(self):
        for obj in self.change_objects:
            self.MapperRegistry.get_mapper(obj).update(obj)

    def delete_objects(self):
        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_update(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)