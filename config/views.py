from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core.files.storage import default_storage
import time
import pathlib
import os
import base64
from .utils.tensorflow.readimage import readImage
from subprocess import Popen

#default path / returns html
def index(response):
    return render(response,"home.html",{})

#POST request for images
def sendImage(request):
    if request.method== 'POST':
        # sets filename equal to time + original filename
        filename = str(round(time.time() * 1000))+str(request.FILES['myfile'])
        filepath = os.path.join(pathlib.Path(__file__).parent.parent.absolute(),'tmp',filename)
        file_obj = request.FILES['myfile']
        #saves file on server in directory tmp
        with default_storage.open('tmp/'+filename, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        #Calls readImage inside utils.tensorflow.readimage folder
        readImage(filepath)
        #Opens newly created image with boxes
        with open('tmp/'+filename,"rb") as f:
            filedata = f.read()
        #Remove image after open deletes from server 
        p = Popen("rm %s" % filepath,shell=True)
        #Returns image
        response = HttpResponse(filedata,content_type="image/png")
        return response
    else:
        return HttpResponse('Page not found')