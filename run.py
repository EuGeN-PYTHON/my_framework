from nst_framework.main import Framework
from urls import routes, fronts
from wsgiref.simple_server import make_server

application = Framework(routes, fronts)

PORT = 8080
HOST = '127.0.0.1'

with make_server('', PORT, application) as serv:
    print(f"Server working: http://{HOST}:{PORT}")
    serv.serve_forever()