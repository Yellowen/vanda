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


from django.conf.urls.defaults import patterns
from views import pkgm_mng
from views import installer
from views import installer_test
from views import desc

urlpatterns = patterns('',
    (r'^$', pkgm_mng),
    
    (r'^installer/test/$', installer_test),
    (r'^installer/apply/' , apply),
    (r'^installer/([A-Za-z0-9]{40})/$', desc),                       
    (r'^installer/$', installer),
)
