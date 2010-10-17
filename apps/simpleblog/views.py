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

from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.core.paginator import Paginator

from models import *


def blog_index (req):
    # TODO: add a filter to retrive last month posts only
    post_list = Post.objects.all ()
    ppp = 10
    if hasattr (Setting, 'post_per_page'):
        ppp = Setting.post_per_page
    paginator = Paginator(post_list, ppp)
    
    try:                                                                                                                                                   
        page = int(req.GET.get('page', '1'))                                                                                                           
    except ValueError:                                                                                                                                     
        page = 1                                                                                                                                       
        
    try:                                                                                                                                                   
        posts = paginator.page(page)                                                                                                                
    except (EmptyPage, InvalidPage):                                                                                                                       
        posts = paginator.page(paginator.num_pages)                                                                                                 
                                                             
    return rr ('blog.html', {"posts" : posts})
