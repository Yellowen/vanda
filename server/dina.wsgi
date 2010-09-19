import os
import sys

try:
	configs = __import__ ("dina.settings", globals(), locals(), [], -1)
except ImportError:
       pass

#if configs.MEDIA_SERVER == "l"
#pid = os.fork ()
pid = 0
if pid:
	pass	
else:
	os.environ['PYTHON_EGG_CACHE'] = '~/.python_egg'
	sys.path.append(os.path.join (os.path.dirname (__file__) , '../').replace ("\\" , "/"))
	os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
	os.environ['DJANGO_MODE'] = 'WSGI'
	print "====> ", os.environ
	import django.core.handlers.wsgi
	application = django.core.handlers.wsgi.WSGIHandler()
