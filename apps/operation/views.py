# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.http import HttpResponse
from filer.models import File, Folder, FolderRoot
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from filer.models import File, Folder, FolderRoot
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import SclMUser
from yunpian.SmsOperator import SmsOperator
import sys
import random
from django.template import Context , loader
APIKEY = '7d30dd097278b7a073e99d548aa54c1d'


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
        can_read_folder = folder.get_childfolder_read(hasuser)
        folderlist = []
        for id in can_read_folder:
            fold = Folder.objects.get(id=id)
            folderlist.append(fold)

        if folder.is_root:
            virtual_items = folder.virtual_folders
        else:
            virtual_items = []


        listoffiledir = list(folder.get_childfile_read(user=hasuser))
        template = loader.get_template('operation/index3.html')
        context = Context({
        'filepath': listoffiledir,
        'foldlist': folderlist,
        })
        return HttpResponse(template.render(context))



class PhoneBindFrom(forms.Form):
    user_phone = forms.CharField(label=u'手机号',max_length=20,)
    verify_code = forms.CharField(label=u'验证码',max_length=20,)


def wx_index(request):
    return render(request, 'operation/wx_index.html')





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
            # 验证码
            verify_code = uform.cleaned_data['verify_code']

            # TODO:待完善
            # 获取session中的手机号
            session_user_phone = request.session.get('session_id_user_phone')
            # 获取session中的验证码
            session_msg_verify_code = request.session.get('session_id_msg_verify_code')
            # 添加到数据库（除验证码之外的其他所需存储的字段）
            # TODO:数据库存储信息
            # SclMUser.objects.create(open_id=open_id, user_phone=user_phone, customerclass=customerclass)
            # 绑定成功，跳转到用户主页
            # TODO:待完善
            # 暂时以session 中的验证码和手机号作为绑定成功的判断条件
            if (user_phone == session_user_phone and verify_code == session_msg_verify_code):
                return HttpResponseRedirect('/operation/wx_index')
            else:
                # TODO:
                return
    else:
        uform = PhoneBindFrom()
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

