# -*- coding: utf-8 -*-
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
from django.conf.urls.defaults import url
from models import Product


urlpatterns = patterns(
    'django.views.generic.list_detail',
    url(r'^product/$', 'object_list',
        {'queryset': Product.objects.all()}),
    url(r'^product/(?P<slug>[-\w]+)/$', 'object_detail',
        {'queryset': Product.objects.all()}))
