from django.shortcuts import render_to_response as rr
from django.http import Http404
from models import *


def blog (request):
    """
    Main view for blog that load in URL request.
    """
    #+++ Blog Config should load here.
    # Blog Config contains some variable about blog actions like number of entry per page
    
    #--- NPP (number per page) should load from configs but now this is for development and will remove in future
    NPP = 4

    ent = post.objects.all ().order_by ("-datetime")[:NPP]
    
    
    return rr ('blog.html' , {"post" : ent})


def comments (request , Slug):
    try:
        p = post.objects.get ( slug = Slug)
    except:
        return Http404 ()
    
    return rr ('comments.html' , {"post" : p})
