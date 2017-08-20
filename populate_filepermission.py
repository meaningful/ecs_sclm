# -*- coding:utf-8 -*-  
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sclmknowledge.settings')

import django
django.setup()

from filer.models.filemodels import FilePermission
from django.contrib.auth.models import User, Group

def populate():
    # 这是拿到已有的组，根据id号
    # g1 = Group.objects.get(id=1)
    # g2 = Group.objects.get(id=2)
    #  创建组
    g1 = Group.objects.create(name='g1')
    g2 = Group.objects.create(name='g2')
    g3 = Group.objects.create(name='g3')
    g4 = Group.objects.create(name='g4')
    
    # # 创建用户,并设置它的组别，注意要用下面两行代码
    user1 = adduser(name='wlw11', password='wlwtest12345')
    user1.groups = (g1,)
    user2 = adduser(name='wlw21', password='wlwtest12345')
    user2.groups = (g2,)
    user3 = adduser(name='wlw31', password='wlwtest12345')
    user3.groups = (g3,)
    user4 = adduser(name='wlw41', password='wlwtest12345')
    user4.groups = (g4,)
 
    fpg1 = addfilepermission(groups=(g1, ),everybody=False,can_edit=1,can_read=0,name='g1e')
    fpg2 = addfilepermission(groups=(g1,),everybody=False,can_edit=0,can_read=1,name='g1r')
    fpg2 = addfilepermission(groups=(g1,g2),everybody=False,can_edit=1,can_read=0,name='g12e')
    fpg3 = addfilepermission(groups=(g1,g2),everybody=False,can_edit=0,can_read=1,name=u'一级二级读')
    fpg4 = addfilepermission(groups=(g1,g2),everybody=False,can_edit=1,can_read=1,name=u'一级二级读写')
    fpg5 = addfilepermission(groups=(g1,g2,g3),everybody=False,can_edit=1,can_read=0,name=u'总代')



# 创建文件权限
def addfilepermission(groups,everybody,can_edit,can_read,name):
    fp = FilePermission.objects.create(everybody=everybody,can_edit=can_edit,can_read=can_read,name=name)
    fp.save()
    fp.groups = groups
    return fp
# 创建用户
def adduser(name,password):
    user = User.objects.create_user(username=name, password=password)
    user.save()
    return user
# Start execution here!
if __name__ == '__main__':
    print "Starting filepermission population script..."
    populate()
