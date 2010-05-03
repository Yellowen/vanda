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
from django.contrib import admin
import os


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
  #  (r'^dpm/', include('dina.core.urls')),
    (r'^core/$', 'dina.core.views.pkgm_mng'),                   
    (r'^menu/menu/$', 'dina.fem.menu.views.change_list'),                   
    (r'^', include(admin.site.urls)),
                       
                       
)
