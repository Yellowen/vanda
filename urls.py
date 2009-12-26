from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect
import confs
import os
from django.conf import settings



#REMOVE:START ----------------
from views import testview
#REMOVEL:END ------------------

urlpatterns = patterns('',
    #REMOVE:START -------------------------------------
    (r'^test$' , testview),
    #REMOVE:END ---------------------------------------
    
                (r'^admin/', include('dina.urls')),
                (r'^$' , 'dina.fem.page.views.show_home'),
                (r'^comments/', include('django.contrib.comments.urls')),

                (r'^' , include('apps.urls')),                                      
                       
)



# this section add site media to the development environment in release time we should use apache for handling this
if settings.DEBUG :
    
    urlpatterns += patterns ('' ,
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': os.path.join ( os.path.dirname (__file__) , 'site_media').replace ('\\' ,'/')}),      
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root':os.path.join ( os.path.dirname (__file__) , 'media').replace ('\\' ,'/')}),
                             
                                                  
)


#+++ here i should find a better way to deal with dynamic urls
plc = confs.urls
if len (plc) != 0:
    for i in plc :
        a = patterns ('' , (i[0] , include (i[1])),)
        print a
        
        urlpatterns += a 


