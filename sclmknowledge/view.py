#coding=utf-8
from django.http import HttpResponse
from django.template import Context , loader
#from filer.models.filemodels import File
from filer.models.foldermodels import Folder

from django.shortcuts import get_list_or_404 , get_object_or_404
import time

def hello(request):
    return HttpResponse("Hello world !  now , the time is :"+ time.strftime('%Y-%m-%d %H-%M-%S'))

def index(request):
    fileindexfolder = get_object_or_404(Folder, name="index_勿删")
    listoffiledir = [singlefile.file for singlefile in fileindexfolder.files ]
    template = loader.get_template('index.html')
    context = Context({
        'filepath':listoffiledir,
    })
    #print template.render(context)
    return HttpResponse(template.render(context))
