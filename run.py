from nst_framework.main import Framework, AppDebug, AppFake
from urls import fronts
from views import routes
from wsgiref.simple_server import make_server

# application = Framework(routes, fronts)
application = AppDebug(routes, fronts)
# application = AppFake(routes, fronts)
PORT = 8880
HOST = '127.0.0.1'

with make_server('', PORT, application) as serv:
    print(f"Server working: http://{HOST}:{PORT}")
    serv.serve_forever()
