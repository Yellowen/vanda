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







from django.template import Template , Context
from django.http import Http404
from models import *
from django.shortcuts import render_to_response as rr

def show_page (request , Slug):
    try:
        a = page.objects.get (slug = Slug)
        #+++ here i add some tag to render for content
        if a.published == True:
            t = Template (a.content).render (Context ())
            title = a.title
            return rr ('index_1.html', {"title" : title , "content" : t})
        else :
            raise Http404 ()
    except:
        raise Http404 ()

def show_home (requset):
    try:
        a = page.objects.get (home = True)
    except:
        #+++ i should add a default home page
        a = page.objects.get (id=1)
    t = Template (a.content).render (Context ())
    title = a.title
    return rr ('index_1.html' , {"title" : title , "content" : t})
