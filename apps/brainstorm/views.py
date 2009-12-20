from django.shortcuts import render_to_response as rr
from django.template import Context , Template
from models import *
from forms import *

def show (request):
    return rr ('test/brainstorm.html')

# i must remove the hidden input
def comments (request , xid):
    if comment in request.POST:
        des = request.POST['description']
        email = request.POST['email']
        Cstorm  = storm.objects.get (id = xid)
        
    else:
        cforms = comment_form (initial = {'storm' : xid})
        return rr ('index_1.html' , {"content" : cforms.as_complete_table () })


