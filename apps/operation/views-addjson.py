# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from filer.models import File, Folder, FolderRoot
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template import RequestContext
from django import forms
from models import SclMUser
from yunpian.SmsOperator import SmsOperator
import sys
import random
import re
from django.urls import reverse
from django.http import JsonResponse
reload(sys)
sys.setdefaultencoding('utf-8')

APIKEY = '7d30dd097278b7a073e99d548aa54c1d'

def index2(request):
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
    return render(request, 'operation/index2.html', context_dict)

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
        # # if folder.is_root and not search_mode:  change whcy
        can_read = folder.get_childfile_read(user=hasuser)
        filelist = list(can_read)
        # filelist = []
        # for num in can_read:
        #     file = File.objects.get(id=num)
        #     filelist.append(file)
        can_read_folder = folder.get_childfolder_read(hasuser)
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
            'user': hasuser,
            'current_url': request.path,
            'folder_children': folderlist, 
            'folder_files': filelist,
        })
        return render(request, 'operation/directory_listing.html', context)

    
class PhoneBindFrom(forms.Form):
    user_phone = forms.CharField(label=u'手机号',max_length=20,)
    verify_code = forms.CharField(label=u'验证码',max_length=20,)


# 本地校验手机号是否绑定
# request 中需携带 open_id & customerclass
def index(request):
    # TODO:1 .接收携带 open_id & customerclass 的 request
    #
    # TODO:2 .根据 open_id 和 customerclass 查询本地数据库中是否已经有绑定的手机号

    # # 重定向至用户界面
    print("已绑定，跳转到用户主页")
    # return render_to_response('index.html', context_instance=RequestContext(request))
    return render(request, 'operation/index.html')


# 手机号绑定
def phone_bind(request):
    if request.method == 'POST':
        uform = PhoneBindFrom(request.POST)
        if uform.is_valid():
            # 获得表单数据
            open_id = u'Wechat_open_id_test1234567890'
            customerclass = u'1'
            # 手机号
            user_phone = uform.cleaned_data['user_phone']
            print("user_phone:" + user_phone)
            # 验证码
            verify_code = uform.cleaned_data['verify_code']
            print("verify_code:" + verify_code)

            # TODO:待完善
            # 获取session中的手机号
            session_user_phone = request.session.get('session_id_user_phone')
            print ("session_user_phone:" + session_user_phone)
            # 获取session中的验证码
            session_msg_verify_code = request.session.get('session_id_msg_verify_code')
            print ("session_id_msg_verify_code:" + session_msg_verify_code)

            print("open_id:" + open_id)
            print("customerclass:" + customerclass)

            # 添加到数据库（除验证码之外的其他所需存储的字段）
            # TODO:待完善
            SclMUser.objects.create(open_id=open_id, user_phone=user_phone, customerclass=customerclass)
            # 绑定成功，跳转到用户主页
            # TODO:待完善
            # 暂时以session 中的验证码和手机号作为绑定成功的判断条件
            if (user_phone == session_user_phone and verify_code == session_msg_verify_code):
                print("绑定成功，跳转到用户主页")
                return HttpResponseRedirect('/operation/index/')
            else:
                print("绑定失败")
                # TODO:
                return
    else:
        uform = PhoneBindFrom()
        print("进行手机绑定")
    context = {}
    context.update({
            'uform': uform,
        })

    return render(request,'operation/phone_bind.html', context)



"""
短信验证码
"""
# 验证码有效期 (验证码有效期设置为15分钟，通Session 有效期保持一致，Session有效期设置在 settings.py 中)
session_age_time = u'15分钟'

# 发送短信验证码
def send_msg(request):
    if request.method == 'GET':
        userPhone = request.GET.get('user_phone')
        request.session['session_id_user_phone'] = userPhone  # 将用户手机号存储到session中
        print userPhone
        verifyCode = generate_verify_code()
        print ("verifyCode:" + verifyCode)
        request.session['session_id_msg_verify_code'] = verifyCode  # 将验证码存储到session中
        # 获取用户手机号等，然后format 短信内容
        msg_info = list([])
        msg_info.append(str(userPhone))
        msg_info.append(verifyCode)
        msg_info.append(session_age_time)
        data = format_msg(str(userPhone), msg_info)
        # API 发送短信
        smsOperator = SmsOperator(APIKEY)
        result = smsOperator.single_send(data)
        return HttpResponse(json.dumps(result.content, ensure_ascii=False), content_type='application/json')


# 随机生成6位数字的验证码
def generate_verify_code():
    code_list = []
    for i in range(6):
        random_num = random.randint(0, 9)
        code_list.append(str(random_num))

    return "".join(code_list)


# 手机号码格式校验
def verify_phone(phone_num):
    phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    return phone_re.match(phone_num)


# 格式化短信内容
def format_msg(phone, l):
    msg_data = {}
    if verify_phone(phone):
        msg_data['mobile'] = str(phone)
    if l.__len__() == 3:
        msg_text = u'【微言信息】亲爱的%s，您的验证码是%s。有效期为%s，请尽快验证' % (l[0],l[1],l[2])
        msg_data['text'] = msg_text
    return msg_data



def indexjson(request):
    fold1 = Folder.objects.get(id=1)
    if request.user:
        user1 = request.user
    else:
        user1 = User.objects.get(id=2)
   # 取得用户user1能读的文件
    can_read = fold1.get_childfile_read(user=user1)
    filelist = []
    for num in can_read:
        file_dict = {}
        if num.name:
            file_dict['name'] = num.name
        else:
            file_dict['name'] = num.label
        file_dict['summary'] = num.description
        file_dict['icon_url'] = num.icons['32']
        file_dict['id'] = num.id
        file_dict['url']= num.url
        file_dict['type'] = num.file_type
        filelist.append(file_dict)
    # 取用户能读的子目录
    can_read_folder = fold1.get_childfolder_read(user1)
    foldlist = []
    for folder_id in can_read_folder:
        folder = Folder.objects.get(id=folder_id)
        folddict = {}
        folddict['id'] = folder.id
        folddict['name'] = folder.name
        folddict['icon_url'] = folder.diricon.url
        folddict['url'] = reverse('directory_listing', args=(folder.id,))
        folddict['type'] = folder.file_type
        foldlist.append(folddict)
    result = []
    result.append(filelist)
    result.append(foldlist)
    # 用模版的返回方法
    # return render(request, 'operation/indexjson.html', {'result': json.dumps(result, ensure_ascii=False )})
    # 用jsonresponse的返回方法
    # return JsonResponse(result, safe=False)
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')

def directory_listing2(request, folder_id=None):
    if request.user:
        hasuser = request.user
    if folder_id is None:
        folder = FolderRoot()
    else:
        folder = get_object_or_404(Folder, id=folder_id)
        # # if folder.is_root and not search_mode:  change whcy
    can_read = folder.get_childfile_read(user=hasuser)
    filelist = []
    for num in can_read:
        file_dict = {}
        if num.name:
            file_dict['name'] = num.name
        else:
            file_dict['name'] = num.label
        file_dict['summary'] = num.description
        file_dict['icon_url'] = num.icons['32']
        file_dict['id'] = num.id
        file_dict['url']= num.url
        file_dict['type'] = num.file_type
        filelist.append(file_dict)
    can_read_folder = folder.get_childfolder_read(user=hasuser)
    foldlist = []
    for child_id in can_read_folder:
        folder = Folder.objects.get(id=child_id)
        folddict = {}
        folddict['id'] = folder.id
        folddict['name'] = folder.name
        folddict['icon_url'] = folder.diricon.url
        folddict['url'] = reverse('directory_listing', args=(folder.id,))
        folddict['type'] = folder.file_type
        foldlist.append(folddict)
    result = []
    result.append(filelist)
    result.append(foldlist)
    # return JsonResponse(result, safe=False)
    # 用httpresponse的返回方法
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


    
