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
    # g1 = Group.objects.create(name='g1')
    # g2 = Group.objects.create(name='g2')
    # g3 = Group.objects.create(name='g3')
    # g4 = Group.objects.create(name='g4')
    g5 = Group.objects.create(name='微信三草两木总代')
    g6 = Group.objects.create(name='微信三草两木官方')
    g7 = Group.objects.create(name="微信三草两木一级代理")
    g8 = Group.objects.create(name='微信三草两木二级代理')
    g9 = Group.objects.create(name='微信三草两木三级代理')
    g10 = Group.objects.create(name='微信三草两木四级代理')
    g11 = Group.objects.create(name='微信珍慕总代')
    g12 = Group.objects.create(name='微信珍慕官方')
    g13= Group.objects.create(name="微信珍慕一级代理")
    g14 = Group.objects.create(name='微信珍慕二级代理')
    g15 = Group.objects.create(name='微信珍慕三级代理')
    g16 = Group.objects.create(name='微信珍慕四级代理')
    
    g17 = Group.objects.create(name='微信清亦总代')
    g18 = Group.objects.create(name='微信清亦官方')
    g19= Group.objects.create(name="微信清亦一级代理")
    g20 = Group.objects.create(name='微信清亦二级代理')
    g21 = Group.objects.create(name='微信清亦三级代理')
    g22 = Group.objects.create(name='微信清亦四级代理')

    g23 = Group.objects.create(name='微信养面膜总代')
    g24 = Group.objects.create(name='微信养面膜官方')
    g25= Group.objects.create(name="微信养面膜一级代理")
    g26 = Group.objects.create(name='微信养面膜二级代理')
    g27 = Group.objects.create(name='微信养面膜三级代理')
    g28 = Group.objects.create(name='微信养面膜四级代理')

    g29 = Group.objects.create(name='微信gbox总代')
    g30 = Group.objects.create(name='微信gbox官方')
    g31 = Group.objects.create(name="微信gbox一级代理")
    g32 = Group.objects.create(name='微信gbox二级代理')
    g33 = Group.objects.create(name='微信gbox三级代理')
    g34 = Group.objects.create(name='微信gbox四级代理')

    # # 创建用户,并设置它的组别，注意要用下面两行代码
    # user1 = adduser(name='wlw11', password='wlwtest12345')
    # user1.groups = (g1,)
    # user2 = adduser(name='wlw21', password='wlwtest12345')
    # user2.groups = (g2,)
    # user3 = adduser(name='wlw31', password='wlwtest12345')
    # user3.groups = (g3,)
    # user4 = adduser(name='wlw41', password='wlwtest12345')
    # user4.groups = (g4,)

    
    user1 = adduser(name='sclmmanager', password='ZSK12ab3456')

    user2 = adduser(name='zmmanager', password='ZSK12ab3456')
    user3 = adduser(name='qymanager', password='ZSK12ab3456')
    user4 = adduser(name='ymmmanager', password='ZSK12ab3456')
    user5 = adduser(name='gboxmanager', password='ZSK12ab3456')
    # fpg1 = addfilepermission(groups=(g1, ),everybody=False,can_edit=1,can_read=0,name='g1e')
    # fpg2 = addfilepermission(groups=(g1,),everybody=False,can_edit=0,can_read=1,name='g1r')
    # fpg2 = addfilepermission(groups=(g1,g2),everybody=False,can_edit=1,can_read=0,name='g12e')
    # fpg3 = addfilepermission(groups=(g1,g2),everybody=False,can_edit=0,can_read=1,name=u'一级二级读')
    # fpg4 = addfilepermission(groups=(g1,g2),everybody=False,can_edit=1,can_read=1,name=u'一级二级读写')
    # fpg5 = addfilepermission(groups=(g1,g2,g3),everybody=False,can_edit=1,can_read=0,name=u'总代')



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
