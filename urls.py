# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) $YEAR$  $AUTHOR$
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------------



from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect

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
                (r'^site_media/(.+)$' ,  'dina.core.server.MediaServ'), 
                (r'^' , include('apps.urls')),                                      
                       
)



# this section add site media to the development environment in release time we should use apache for handling this
#if settings.DEBUG :
    
#    urlpatterns += patterns ('' ,
 #                      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': os.path.join ( os.path.dirname (__file__) , 'site_media').replace ('\\' ,'/')}),      
  #                     (r'^media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root':os.path.join ( os.path.dirname (__file__) , 'media').replace ('\\' ,'/')}),
                             
                                                  
#)

