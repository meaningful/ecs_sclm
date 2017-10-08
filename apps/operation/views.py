# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import re
import sys
import requests
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
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.template import loader, Context
from xml.etree import ElementTree as ET
import time
import hashlib
import lxml
from lxml import etree
import urllib2
import json
from django.urls import reverse
reload(sys)
sys.setdefaultencoding('utf-8')
#APIKEY = '7d30dd097278b7a073e99d548aa54c1d'
APIKEY = '6dfa92857a0c6c6c963b42e0f09e1565'
global appid
global appsecret

appid = "wx8ca0d078587b5a8e"
appsecret = "c9eb23fa299124647ed3298030e6215e"

class WeChat(View):
  #这里我当时写成了防止跨站请求伪造，其实不是这样的，恰恰相反。因为django默认是开启了csrf防护中间件的
  #所以这里使用@csrf_exempt是单独为这个函数去掉这个防护功能。
  @csrf_exempt
  def dispatch(self, *args, **kwargs):
    return super(WeChat, self).dispatch(*args, **kwargs)
    
  def get(self, request):
  
    #下面这四个参数是在接入时，微信的服务器发送过来的参数
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    
    #这个token是我们自己来定义的，并且这个要填写在开发文档中的Token的位置
    token = 'sclm2017'
    
    #把token，timestamp, nonce放在一个序列中，并且按字符排序
    hashlist = [token, timestamp, nonce]
    hashlist.sort()
    
    #将上面的序列合成一个字符串
    hashstr = ''.join([s for s in hashlist])
    
    #通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
    hashstr = hashlib.sha1(hashstr).hexdigest()
    
    #把我们生成的字符串和微信服务器发送过来的字符串比较，
    #如果相同，就把服务器发过来的echostr字符串返回去
    if hashstr == signature:
      return HttpResponse(echostr)


# 前端表单
class WeChatBindFrom(forms.Form):
    agent_wx = forms.CharField(label=u'微信号', max_length=50,)
    verify_code = forms.CharField(label=u'验证码', max_length=6,)


# open_id = u'open_id123'
customerclass = u'微信三草两木'


def index(request):
    # fold1 = Folder.objects.get(id=1)
    # if request.user:
    #     user1 = request.user
    # else:
    #     user1 = User.objects.get(id=2)
    # context_dict = {'foldermessage': fold1.file_count}
    # # Return a rendered response to send to the client.
    # # We make use of the shortcut function to make our lives easier.
    # # Note that the first parameter is the template we wish to use.
    # context_dict['usermessage'] = user1.username
    # can_read = fold1.get_childfile_read(user=user1)
    # context_dict['canreadfilelist'] = list(can_read)
    # context_dict['fold'] = fold1
    # can_read_folder = fold1.get_childfolder_read(user=user1)
    # folderlist = []
    # for id in can_read_folder:
    #     folder = Folder.objects.get(id=id)
    #     folderlist.append(folder)
    # context_dict['foldlist'] = folderlist
    # return render(request, 'operation/index.html', context_dict)
    code = request.GET.get('code', None)
    open_id = get_openid(appid,appsecret,code)
    request.session['open_id'] = open_id
    result_tab_zsk_userinfo = DBHelper.query(DBHelper.sql_tab_zsk_userinfo.format("\'"+open_id+"\'"))
    if not result_tab_zsk_userinfo or result_tab_zsk_userinfo.__len__() == 0:
        return  HttpResponseRedirect('/operation/phone_bind/')
    else:
        user_info = get_user_info(str(result_tab_zsk_userinfo[0][0]), customerclass)
        agent_levename = user_info[1]
        if agent_levename:
            group = format_group(str(customerclass)+str(agent_levename))
            request.session['user_group'] = group
            return  HttpResponseRedirect(reverse('directory_listing',args=(1,)))
            
    
def get_openid(appid,appsecret,code):
    # print("*************************test******************************")
    response = urllib2.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code&connect_redirect=1'%(appid,appsecret,code))
    content = response.read()
    s=json.loads(content)
    # return HttpResponse("Hello, %s"%s["openid"])
    return s["openid"]

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
        hasgroup = request.session.get('user_group')
        folderlist = []
        # hasgroup = request.GET.get('group')
        if hasgroup:
            listoffiledir = list(folder.get_childfile_read(group=hasgroup))
            can_read_folder = folder.get_childfolder_read(group=hasgroup)
            for id in can_read_folder:
                fold = Folder.objects.get(id=id)
                folderlist.append(fold)
        else:
            if request.user:
                hasuser = request.user
                listoffiledir = list(folder.get_childfile_read(user=hasuser))
                can_read_folder = folder.get_childfolder_read(user=hasuser)
                for id in can_read_folder:
                    fold = Folder.objects.get(id=id)
                    folderlist.append(fold)
        
        #     if request.GET.get('group'):
        #         hasgroup = request.GET.get('group')
        #         listoffiledir = list(folder.get_childfile_read(group=hasgroup))
        #         can_read_folder = folder.get_childfolder_read(group=hasgroup)
        #         for id in can_read_folder:
        #             fold = Folder.objects.get(id=id)
        #             folderlist.append(fold)
        #
        if folder.is_root:
            virtual_items = folder.virtual_folders
        else:
            virtual_items = []


        template = loader.get_template('wxWeb/index.html')
        context = Context({
        'filepath': listoffiledir,
        'foldlist': folderlist,
        })
        return HttpResponse(template.render(context))


# def directory_listing(request, folder_id=None):
#         if folder_id is None:
#             folder = FolderRoot()
#         else:
#             folder = get_object_or_404(Folder, id=folder_id)
#         request.session['filer_last_folder_id'] = folder_id

#         folderlist = []
#         if request.user:
#             hasuser = request.user
#             listoffiledir = list(folder.get_childfile_read(user=hasuser))
#             can_read_folder = folder.get_childfolder_read(user=hasuser)
#             for id in can_read_folder:
#                 fold = Folder.objects.get(id=id)
#                 folderlist.append(fold)
#         else:
#             if request.group:
#                 hasgroup = request.group
#                 listoffiledir = list(folder.get_childfile_read(group=hasgroup))
#                 can_read_folder = folder.get_childfolder_read(group=hasgroup)
#                 for id in can_read_folder:
#                     fold = Folder.objects.get(id=id)
#                     folderlist.append(fold)
   
#         if folder.is_root:
#             virtual_items = folder.virtual_folders
#         else:
#             virtual_items = []


#         template = loader.get_template('operation/index3.html')
#         context = Context({
#         'filepath': listoffiledir,
#         'foldlist': folderlist,
#         })
#         return HttpResponse(template.render(context))


# 手机号绑定
def phone_bind(request):
    if request.method == 'POST':
        open_id = request.session.get('open_id')
        uform = WeChatBindFrom(request.POST)
        if uform.is_valid():
            # 从表单中获获取agent_wx 和 验证码
            agent_wx = uform.cleaned_data['agent_wx']
            verify_code = uform.cleaned_data['verify_code']
            # 获取session中的agent_wx 和 验证码
            session_agent_wx = request.session.get('session_id_agent_wx')
            session_msg_verify_code = request.session.get('session_id_msg_verify_code')
	    if not open_id or not agent_wx or not session_agent_wx or not verify_code or not session_msg_verify_code:
                return render(request,'operation/phone_bind_error.html',{})
            # 以session 中的验证码和微信号一致为绑定成功的判断条件
            if agent_wx == session_agent_wx and verify_code == session_msg_verify_code:
                DBHelper.insert(
                    DBHelper.sql_tab_zsk_userinfo_insert.format("\'" + open_id + "\'", "\'" + agent_wx + "\'"))
                user_info = get_user_info(agent_wx, customerclass)
                group = format_group(str(customerclass) + str(user_info[1]))
                request.session['user_group'] = group
                # return requests.post(settings.ALLOWED[0]+reverse('directory_listing',args=(1,)), data=json.dumps({'group': group}))
                # return HttpResponseRedirec
                # t('/operation/1/?group='+group)
                return  HttpResponseRedirect(reverse('directory_listing',args=(1,)))
                # return HttpResponseRedirect('/operation/1/')
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
# 验证码有效期 (验证码有效期设置为10分钟，通Session 有效期保持一致，Session有效期设置在 settings.py 中)
session_age_time = u'10分钟'

# 发送短信验证码
def send_msg(request):
    if request.method == 'GET':
        agent_wx = request.GET.get('agent_wx')
        request.session['session_id_agent_wx'] = agent_wx
        
        user_info = get_user_info(agent_wx, customerclass)
        user_phone = user_info[0]
        if not user_phone:
            result = {u'msg': u'该微信号尚未成为正式代理/经销商，请检查后再次输入！'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')

        verify_code = generate_verify_code()
        # 将验证码存储到session中
        request.session['session_id_msg_verify_code'] = verify_code
        # format 短信内容
        msg_info = list([])
        msg_info.append(verify_code)
        msg_info.append(session_age_time)
        data = format_msg(str(user_phone), msg_info)
        # API 发送短信
        smsOperator = SmsOperator(APIKEY)
        result = smsOperator.single_send(data)
        if result.content["code"] == 0:
            result.content["msg"] = u'验证码已发送至尾号:'+str(user_phone)[-4:]+u'的手机,请注意查收！'
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
    if l.__len__() == 2:
        msg_text = u'【上海传美】欢迎使用传美知识库，您的手机验证码是%s，有效期为%s，如非本人操作请忽略本信息。' % (l[0],l[1])
        msg_data['text'] = msg_text
    return msg_data


# 格式化group参数
def format_group(group):
    str_wx = '微信'
    str_zt = '总代'
    str_ztl = '总代理'

    if str(group).find('微信') != 0:
        group = str_wx + str(group)

    if str(group).find(str_ztl) != 0:
        group = str(group).replace(str_ztl, str_zt)

    return str(group)







