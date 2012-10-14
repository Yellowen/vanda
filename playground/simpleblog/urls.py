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
from django.conf.urls.defaults import include
from django.conf.urls.defaults import url
from feed import LatestPosts


urlpatterns = patterns('',
    (r'^$', 'apps.simpleblog.views.blog_index'),
    (r'^feed/$', LatestPosts()),
    (r'^post/([^/]+)/$', 'apps.simpleblog.views.post_view'),
    (r'^category/([^/]+)/$', 'apps.simpleblog.views.category_index'),
    (r'^comment/([^/]+)/$', 'apps.simpleblog.views.post_comment'),
    url(r'^captcha/', include('captcha.urls')),
)