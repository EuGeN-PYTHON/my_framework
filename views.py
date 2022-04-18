from datetime import date

from nst_framework.templator import render
from main_pattern.engine_project import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render('main.html', style=request.get('style', None), data=request.get('data', None))


class About:
    def __call__(self, request):
        return '200 OK', render('wait.html', data=request.get('data', None))


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', data=request.get('data', None))


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Towers:
    def __call__(self, request):
        return '200 OK', render('towers.html', objects_list=site.typeobject)


class TowersList:
    def __call__(self, request):
        logger.log('Список объектов')
        try:
            typeobject = site.find_type_by_id(int(request['request_params']['id']))
            return '200 OK', render('tower_list.html', objects_list=typeobject.objects, name=typeobject.name,
                                    id=typeobject.id)
        except KeyError:
            return '200 OK', 'No objects have been added yet'


class TypeList:
    def __call__(self, request):
        logger.log('Список типов объектов')
        return '200 OK', render('type_list.html', objects_list=site.typeobject)


class CopyObject:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_object = site.get_object(name)
            if old_object:
                new_name = f'copy_{name}'
                new_object = old_object.clone()
                new_object.name = new_name
                site.objects.append(new_object)
            return '200 OK', render('tower_list.html', objects_list=site.objects)
        except KeyError:
            return '200 OK', 'No objects have been added yet'


class CreateObject:
    type_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            typeobject = None
            if self.type_id != -1:
                typeobject = site.find_type_by_id(int(self.type_id))
                object = site.create_object('pillar', typeobject, name)
                site.objects.append(object)

            return '200 OK', render('tower_list.html', objects_list=typeobject.objects,
                                    name=typeobject.name, id=typeobject.id)
        else:
            try:
                self.type_id = int(request['request_params']['id'])
                typeobject = site.find_type_by_id(int(self.type_id))
                return '200 OK', render('create_object.html', name=typeobject.name, id=typeobject.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


class CreateType:
    def __call__(self, request):
        if request['method'] == 'POST':
            print(request)
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            type_id = data.get('category_id')

            type = None
            if type_id:
                category = site.find_type_by_id(int(type_id))

            new_type = site.create_type(name, type)
            site.typeobject.append(new_type)

            return '200 OK', render('towers.html', objects_list=site.typeobject)
        else:
            typeobject = site.typeobject
            return '200 OK', render('create_type.html', categories=typeobject)
