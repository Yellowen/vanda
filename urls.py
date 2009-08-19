from django.conf.urls.defaults import *

import confs
from django.contrib import admin
import os

from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^Dina_CMS/', include('Dina_CMS.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)



# this section add site media to the development environment in release time we should use apache for handling this
if settings.DEBUG :
    
    urlpatterns += patterns ('' ,
                             (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root':os.path.join ( os.path.dirname (__file__) , 'media').replace ('\\' ,'/')}),
                             
                                                  
)


#+++ here i should find a better way to deal with dynamic urls

#conf = settings.FS_ROOT + "/confs/urls"
#fd = open (conf , 'r')
#urls = fd.readlines ()

#fd.close ()
#!!! may be i should use something other that patterns ('' , '')
#a = patterns ('' , '')
plc = confs.urls
if len (plc) != 0:
    for i in plc :
        a = patterns ('' , (i[0] , include (i[1])),)
        print a
        
        urlpatterns += a 


