"""
WSGI config for sclmknowledge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
#sys.path.append('/usr/lib/python2.7/site-packages')  
#sys.path.append('/usr/lib64/python2.7/site-packages') 

status = '200 OK'

output = 'sys.path = %s\n' % repr(sys.path)
output += 'sys.version = %s\n' % repr(sys.version)
output += 'sys.prefix = %s\n' % repr(sys.prefix)

print output
sys.path = ['/home/media','/root/WorkSpace/sclmknowledge/extra_apps', '/root/WorkSpace/sclmknowledge/apps', '/root/WorkSpace/sclmknowledge', '/usr/local/lib/python2.7/dist-packages/AliyunUtil-0.0.1-py2.7.egg', '/usr/local/lib/python2.7/dist-packages/cloud_init-0.7.6-py2.7.egg', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-x86_64-linux-gnu', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages', '/usr/lib/python2.7/site-packages', '/usr/lib64/python2.7/site-packages']



from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sclmknowledge.settings")

application = get_wsgi_application()
