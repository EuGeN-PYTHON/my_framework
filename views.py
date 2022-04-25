from datetime import date

from nst_framework.templator import render
from main_pattern.engine_project import Engine, Logger, MapperRegistry
from main_pattern.decors_project import GetDebug, GetRoute
from main_pattern.notifier_project import EmailNotifier, SmsNotifier, \
    TemplateView, ListView, CreateView, BaseSerializer
from main_pattern.unit_of_work import UnitOfWork

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


routes = {}


@GetRoute(routes=routes, url='/')
class Index:
    @GetDebug(name='Index')
    def __call__(self, request):
        return '200 OK', render('main.html', style=request.get('style', None), data=request.get('data', None))


@GetRoute(routes=routes, url='/about/')
class About:
    @GetDebug(name='About')
    def __call__(self, request):
        return '200 OK', render('wait.html', data=request.get('data', None))


@GetRoute(routes=routes, url='/contact/')
class Contact:
    @GetDebug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html', data=request.get('data', None))


class NotFound404:
    @GetDebug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@GetRoute(routes=routes, url='/towers/')
class Towers:
    @GetDebug(name='Towers')
    def __call__(self, request):
        return '200 OK', render('towers.html', objects_list=site.typeobject)


@GetRoute(routes=routes, url='/towers-list/')
class TowersList:
    @GetDebug(name='TowersList')
    def __call__(self, request):
        logger.log('Список объектов')
        try:
            typeobject = site.find_type_by_id(int(request['request_params']['id']))
            return '200 OK', render('tower_list.html', objects_list=typeobject.objects, name=typeobject.name,
                                    id=typeobject.id)
        except KeyError:
            return '200 OK', 'No objects have been added yet'


@GetRoute(routes=routes, url='/type-list/')
class TypeList:
    @GetDebug(name='TypeList')
    def __call__(self, request):
        logger.log('Список типов объектов')
        return '200 OK', render('type_list.html', objects_list=site.typeobject)


@GetRoute(routes=routes, url='/copy-object/')
class CopyObject:
    @GetDebug(name='CopyObject')
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


@GetRoute(routes=routes, url='/create-object/')
class CreateObject:
    type_id = -1

    @GetDebug(name='CreateObject')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            typeobject = None
            if self.type_id != -1:
                typeobject = site.find_type_by_id(int(self.type_id))
                object = site.create_object('pillar', typeobject, name)
                object.observers.append(email_notifier)
                object.observers.append(sms_notifier)
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


@GetRoute(routes=routes, url='/create-type/')
class CreateType:
    type_id = None

    @GetDebug(name='CreateType')
    def __call__(self, request):
        if request['method'] == 'GET':
            request_params = request['request_params']
            if request_params != '':
                self.type_id = request_params.get('id')

        if request['method'] == 'POST':
            print(request)
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            # type_id = data.get('category_id')

            type_object = None

            new_type = site.create_type(name, type_object)
            if self.type_id != None:
                type_object = site.find_type_by_id(int(self.type_id))
                type_object.typeobject = new_type

            site.typeobject.append(new_type)

            return '200 OK', render('towers.html', objects_list=site.typeobject)
        else:
            typeobject = site.typeobject
            return '200 OK', render('create_type.html', categories=typeobject)


@GetRoute(routes=routes, url='/client-list/')
class ClientListView(ListView):
    # queryset = site.clients
    template_name = 'client_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('client')
        return mapper.all()

@GetRoute(routes=routes, url='/create-client/')
class ClientCreateView(CreateView):
    template_name = 'create_client.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        email = data['email']
        new_client = site.create_user('client', name, email)
        site.clients.append(new_client)
        new_client.mark_new()
        UnitOfWork.get_current().commit()


@GetRoute(routes=routes, url='/add-client/')
class AddClientByObjectCreateView(CreateView):
    template_name = 'add_client.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['objects'] = site.objects
        context['clients'] = site.clients
        return context

    def create_obj(self, data: dict):
        object_name = data['object_name']
        object_name = site.decode_value(object_name)
        object = site.get_object(object_name)
        client_name = data['client_name']
        client_name = site.decode_value(client_name)
        client = site.get_student(client_name)
        object.add_client(client)


@GetRoute(routes=routes, url='/api/')
class ObjectApi:
    @GetDebug(name='ObjectApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.objects).save()
