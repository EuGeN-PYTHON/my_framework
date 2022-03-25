from nst_framework.main import Framework
from urls import routes, fronts
from wsgiref.simple_server import make_server

application = Framework(routes, fronts)

with make_server('', 8080, application) as serv:
    print("Запуск на 8888 порту...")
    serv.serve_forever()