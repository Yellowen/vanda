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
            return rr ('default/index_1.html', {"title" : title , "content" : t})
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
    return rr ('default/index_1.html' , {"title" : title , "content" : t})
