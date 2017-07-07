from __future__ import unicode_literals
import re
from django.http import HttpResponse
from django.shortcuts import render
from filer.models import File, Folder, FolderRoot
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    fold1 = Folder.objects.get(id=1)
    if request.user:
        user1 = request.user
    else:
        urser1 = User.objects.get(id=2)
    context_dict = {'foldermessage': fold1.file_count}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    context_dict['usermessage'] = user1.username
    can_read = fold1.get_childfile_read(user=user1)
    # readlist = []
    # for num in can_read:
    #     file = File.objects.get(id=num)
    #     readlist.append(file)
    # context_dict['canreadfilelist'] = json.dumps(can_readlist)
    # context_dict['canreadfilelist'] = readlist
    context_dict['canreadfilelist'] = list(can_read)
    context_dict['fold'] = fold1
    can_read_folder = fold1.get_childfolder_read(user1)
    folderlist = []
    for id in can_read_folder:
        folder = Folder.objects.get(id=id)
        folderlist.append(folder)
    context_dict['foldlist'] = folderlist
    return render(request, 'operation/index.html', context_dict)

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/operation/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'operation/login.html', {})
    # Create your views here.  

def directory_listing(request, folder_id=None):
        if request.user:
            hasuser = request.user
        if folder_id is None:
            folder = FolderRoot()
        else:
            folder = get_object_or_404(Folder, id=folder_id)
        request.session['filer_last_folder_id'] = folder_id
        # actions = self.get_actions(request)
        # folder_qs = folder.children.all()
        # file_qs = folder.files.all()
        # show_result_count = False
        # folder_children = folder_qs
        # folder_files = file_qs
        # # if folder.is_root and not search_mode:  change whcy
        can_read = folder.get_childfile_read(user=hasuser)
        filelist = list(can_read)
        # filelist = []
        # for num in can_read:
        #     file = File.objects.get(id=num)
        #     filelist.append(file)
        can_read_folder = folder.get_childfolder_read(user)
        folderlist = []
        for id in can_read_folder:
            fold = Folder.objects.get(id=id)
            folderlist.append(fold)

        if folder.is_root:
            virtual_items = folder.virtual_folders
        else:
            virtual_items = []

        context = {}
        context.update({
            'folder': folder,
            'user': user,
            'current_url': request.path,
            'folder_children': folderlist, 
            'folder_files': filelist,
        })
        return render(request, 'operation/directory_listing.html', context)

