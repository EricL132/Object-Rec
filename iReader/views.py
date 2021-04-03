from django.shortcuts import render
from django.http import HttpResponse


def index(response):
    return render(response,"home.html",{})

def sendImage(request):
    if request.method== 'POST':
        return HttpResponse('')
    else:
        return HttpResponse('Page not found')