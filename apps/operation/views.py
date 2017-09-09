# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import re
import sys

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from filer.models import Folder, FolderRoot
from yunpian.SmsOperator import SmsOperator
from django.template import Context , loader
from .utils import DBHelper
reload(sys)
sys.setdefaultencoding('utf-8')
APIKEY = '7d30dd097278b7a073e99d548aa54c1d'


# 前端表单
class WeChatBindFrom(forms.Form):
    agent_wx = forms.CharField(label=u'微信号', max_length=50,)
    verify_code = forms.CharField(label=u'验证码', max_length=6,)


open_id = u'open_id123'
customerclass = u'微信三草两木'


def index(request):
    fold1 = Folder.objects.get(id=1)
    if request.user:
        user1 = request.user
    else:
        user1 = User.objects.get(id=2)
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
    can_read_folder = fold1.get_childfolder_read(user=user1)
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
        if folder_id is None:
            folder = FolderRoot()
        else:
            folder = get_object_or_404(Folder, id=folder_id)
        request.session['filer_last_folder_id'] = folder_id

        folderlist = []
        if request.user:
            hasuser = request.user
            listoffiledir = list(folder.get_childfile_read(user=hasuser))
            can_read_folder = folder.get_childfolder_read(user=hasuser)
            for id in can_read_folder:
                fold = Folder.objects.get(id=id)
                folderlist.append(fold)
        else:
            if request.group:
                hasgroup = request.group
                listoffiledir = list(folder.get_childfile_read(group=hasgroup))
                can_read_folder = folder.get_childfolder_read(group=hasgroup)
                for id in can_read_folder:
                    fold = Folder.objects.get(id=id)
                    folderlist.append(fold)
   
        if folder.is_root:
            virtual_items = folder.virtual_folders
        else:
            virtual_items = []


        template = loader.get_template('operation/index3.html')
        context = Context({
        'filepath': listoffiledir,
        'foldlist': folderlist,
        })
        return HttpResponse(template.render(context))


# 手机号绑定
def phone_bind(request):
    if request.method == 'POST':
        uform = WeChatBindFrom(request.POST)
        if uform.is_valid():
            # 从表单中获获取agent_wx 和 验证码
            agent_wx = uform.cleaned_data['agent_wx']
            verify_code = uform.cleaned_data['verify_code']
            # 获取session中的agent_wx 和 验证码
            session_agent_wx = request.session.get('session_id_agent_wx')
            session_msg_verify_code = request.session.get('session_id_msg_verify_code')
            # 以session 中的验证码和微信号一致为绑定成功的判断条件
            if agent_wx == session_agent_wx and verify_code == session_msg_verify_code:
                DBHelper.insert(
                    DBHelper.sql_tab_zsk_userinfo_insert.format("\'" + open_id + "\'", "\'" + agent_wx + "\'"))
                user_info = get_user_info(agent_wx, customerclass)
                group = format_group(str(customerclass) + str(user_info[1]))
                return HttpResponseRedirect('/operation/1/?group='+group)
            else:
                return HttpResponseRedirect('/operation/phone_bind/')
    else:
        uform = WeChatBindFrom()
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
        agent_wx = request.GET.get('agent_wx')
        request.session['session_id_agent_wx'] = agent_wx
        
        user_info = get_user_info(agent_wx, customerclass)
        user_phone = user_info[0]
        if not user_phone:
            result = {u'msg': u'绑定的手机号有误或者不存在！'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')

        verify_code = generate_verify_code()
        # 将验证码存储到session中
        request.session['session_id_msg_verify_code'] = verify_code
        # format 短信内容
        msg_info = list([])
        msg_info.append(str(user_phone))
        msg_info.append(verify_code)
        msg_info.append(session_age_time)
        data = format_msg(str(user_phone), msg_info)
        # API 发送短信
        smsOperator = SmsOperator(APIKEY)
        result = smsOperator.single_send(data)
        if result.content["code"] == 0:
            result.content["msg"] = u'验证码已发送至:'+str(user_phone)+u',请注意查收！'
        return HttpResponse(json.dumps(result.content, ensure_ascii=False), content_type='application/json')


# 查询用户信息
def get_user_info(agent_wx, customerclass):
    user_phone = None
    # 查询agent表
    result_tab_agent = DBHelper.query(
        DBHelper.sql_tab_agent.format("\'" + agent_wx + "\'", "\'" + customerclass + "\'"))
    if not result_tab_agent or result_tab_agent.__len__() == 0:
        # 查询 authorinfo 表
        result_tab_authinfo = DBHelper.query(DBHelper.sql_tab_authinfo.format("\'" + agent_wx + "\'"))
        if not result_tab_authinfo or result_tab_authinfo.__len__() == 0:
            # agent 和 authinfo 都查询不到,agent_levename 为游客
            agent_levelname = u'Guest'
            return [user_phone, agent_levelname]
        else:
            user_phone = result_tab_authinfo[0][0]
            agent_levelname = result_tab_agent[0][1]
            return [user_phone, agent_levelname]
    else:
        user_phone = result_tab_agent[0][0]
        agent_levelname = result_tab_agent[0][1]
       
    return [user_phone, agent_levelname]


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


# 格式化group参数
def format_group(group):
    if str(group).find(u'微信') ==0:
        group = str(group).replace(u'微信', '')
    
    if str(group).find(u'总代') !=0:
        group = str(group).replace(u'总代', u'总代理')
        
    if str(group).find(u'官方') !=0:
        group = str(group).replace(u'官方', u'总代理')
        
    return str(group)







