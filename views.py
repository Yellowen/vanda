# -----------------------------------------------------------------------------
#    Vanda Project 
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
# -----------------------------------------------------------------------------
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response as rr
from models import Post

def home(request):
    
    """
    Main view of blog.
    """
    #+++ Blog Config should load here.
    # Blog Config contains some variable about blog
    #actions like number of entry per page

    #--- NPP (number per page) should load from
    #configs but now this is for development and will remove in future
    
    NPP = 4

    ent = Post.objects.all().order_by("-datetime")[:NPP]
    return rr('blog.html', {"post": ent})


def blog(request):
    """
    Main view of one type of blog posts.
    """
    #+++ Blog Config should load here.
    # Blog Config contains some variable about blog
    #actions like number of entry per page

    #--- NPP (number per page) should load from
    #configs but now this is for development and will remove in future
    NPP = 4

    ent = Post.objects.all().order_by("-datetime")[:NPP]
    return rr('blog.html', {"post": ent})


def comments(request, slug):
    get_object_or_404(Post, slug=slug)
    render = {"post": Post, }
    render.update(csrf(request))
    #for fixing bug#29883
    return rr('comments.html', render)
