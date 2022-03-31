from nst_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('main.html', style=request.get('style', None), data=request.get('data', None))


class About:
    def __call__(self, request):
        return '200 OK', render('wait.html', data=request.get('data', None))

class Towers:
    def __call__(self, request):
        return '200 OK', render('wait.html', data=request.get('data', None))

class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', data=request.get('data', None))


# class NotFound404:
#     def __call__(self, request):
#         return '404 WHAT', '404 PAGE Not Found'