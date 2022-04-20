from time import time


class GetRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class GetDebug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def wrapper(method):
            def timed(*args, **kw):
                start = time()
                result = method(*args, **kw)
                end = time()
                delta_time = end - start

                print(f'debug --> {self.name} выполнялся {delta_time:2.2f} ms')
                return result

            return timed

        return wrapper(cls)
