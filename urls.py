from datetime import date
from views import Index, About, Contact, TowersList, CreateObject, CreateType, TypeList, CopyObject, Towers


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


# def style(request):
#     with open('templates/css/style.css') as file:
#         css_file = file.read()
#     request['style'] = css_file


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    '/towers/': Towers(),
    '/towers-list/': TowersList(),
    '/create-object/': CreateObject(),
    '/create-type/': CreateType(),
    '/type-list/': TypeList(),
    '/copy-object/': CopyObject()
}
