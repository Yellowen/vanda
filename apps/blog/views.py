from django.shortcuts import render_to_response as rr
from models import *


def blog (request):
    """
    Main view for blog that load in URL request.
    """
    #+++ Blog Config should load here.
    # Blog Config contains some variable about blog actions like number of entry per page
    
    #--- NPP (number per page) should load from configs but now this is for development and will remove in future
    NPP = 10

    ent = entry.objects.all ().order_by ("datetime")[:NPP]
    
    
    return rr ('blog.html' , {"entry" : ent})
