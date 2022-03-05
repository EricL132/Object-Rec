from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core.files.storage import default_storage
import time
import pathlib
import os
import base64
from .modules.ten.readimage import readImage
from subprocess import Popen


def index(response):
    return render(response,"home.html",{})

def sendImage(request):
    if request.method== 'POST':
        filename = str(round(time.time() * 1000))+str(request.FILES['myfile']) # received file name
        file_obj = request.FILES['myfile']
        with default_storage.open('tmp/'+filename, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        readImage(os.path.join(pathlib.Path(__file__).parent.parent.absolute(),'tmp',filename))
        with open('tmp/'+filename,"rb") as f:
            filedata = f.read()
        p = Popen("rm %s" % os.path.join(pathlib.Path(__file__).parent.parent.absolute(),'tmp',filename),shell=True)
        response = HttpResponse(filedata,content_type="image/png")
        return response
    else:
        return HttpResponse('Page not found')