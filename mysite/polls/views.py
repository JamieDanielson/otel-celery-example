from django.http import HttpResponse
from mysite.celery import print_hello

def index(request):
    hello = print_hello.delay().get()
    return HttpResponse(hello)