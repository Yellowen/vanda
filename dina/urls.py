# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
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

import os

from django.conf.urls.defaults import *
from django.contrib import admin
from django.utils.functional import update_wrapper


from dina.core.sites import admin_index


admin.autodiscover()



def wrap(view, cacheable=False):
    def wrapper(*args, **kwargs):
        return admin.site.admin_view(view, cacheable)(*args, **kwargs)
    return update_wrapper(wrapper, view)
        

urlpatterns = patterns('',

    # (r'^dpm/', include('dina.core.urls')),
    (r'^core/$', 'dina.core.views.pkgm_mng'),                   
    (r'^menu/menu/$', 'dina.fem.menu.views.change_list'),
    # regex should change according to django naming policy
    (r'^([A-Za-z][A-Za-z0-9]{1,30})/config/$', 'dina.conf.views.conf_view'),    
    url(r'^$', wrap(admin_index), name='index'),
    (r'^', include(admin.site.urls)),
)
