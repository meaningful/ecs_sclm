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
    fileindexfolder = get_object_or_404(Folder, name="ab")
    # listoffiledir = [singlefile.file for singlefile in fileindexfolder.files ]
    hasuser = 'sclmmanager'
    listoffiledir = list(fileindexfolder.get_childfile_read())
    can_read_folder = list(fileindexfolder.get_childfolder_read())
#    can_read_folder = fileindexfolder.get_children()
    folderlist = []
    for id in can_read_folder:
    	fold = Folder.objects.get(id=id)
	folderlist.append(fold)
    template = loader.get_template('wxWeb/index.html')
    context = Context({
        'filepath':listoffiledir,
	'foldlist': folderlist,
    })
    #print template.render(context)
    return HttpResponse(template.render(context))
