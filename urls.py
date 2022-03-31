from datetime import date
from views import Index, About, Contact, Towers


# front controller
def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'

def style(request):
    with open('templates/css/style.css') as file:
        css_file = file.read()
    request['style'] = css_file


fronts = [secret_front, other_front, style]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    '/towers/': Towers()
}
