import os
import sys

# WARNING: Serving media files via the same process as dina is performance bottlenect
# we should able to serve media from another server of we have to fork some process
# to run media server 


# TODO: Build some process for serving media


os.environ['PYTHON_EGG_CACHE'] = '~/.python_egg'
sys.path.append(os.path.join (os.path.dirname (__file__) , '../').replace ("\\" , "/"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['DJANGO_MODE'] = 'WSGI'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
