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


from django.template import Template , Context
from django.http import Http404
from models import page
from models import category
from models import section
from django.shortcuts import render_to_response as rr


def show_page (request , Slug):
    try:
        a = page.objects.get (slug=Slug)
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
        a = page.objects.get (home=True)
    except:
        #+++ i should add a default home page
        a = page.objects.get (id=1)
    t = Template (a.content).render (Context ())
    title = a.title
    return rr ('index_1.html' , {"title" : title , "content" : t})


def show_section (requset , Slug):
    try:
        section_info = section.objects.get (slug=Slug)
        section_all = section.objects.filter (published=True)
        category_all = category.objects.filter (published=True , section=section_info)
        return rr ("section.html" , {"section_all" : section_all , "category_all" : category_all , "section_info" : section_info})
    except:
        raise Http404 ()


def show_category (requset , Slug):
    try:
        category_info = category.objects.get (slug=Slug)
        category_all = category.objects.filter (published=True)
        page_all = page.objects.filter (published=True , category=category_info)
        return rr ("category.html" , {"category_all" : category_all , "page_all" : page_all , "category_info" : category_info})
    except:
        raise Http404 ()
