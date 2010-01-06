from django.shortcuts import render_to_response as rr
from django.template import Context , Template
from django.template.loader import get_template
from models import *
from forms import *
from django.utils.translation import ugettext as _


def show (request):
    if 'email' in request.POST:
        cat = category.objects.get (id = int (request.POST['category']))
        st = storm (email = request.POST['email'] , title = request.POST['storm'] , published = False , description = request.POST['description'] , category = cat )
        st.save ()
        return rr ('default/index_1.html' , {"content" :   _("Your storm Commited , thanks for sharing.")})
    else:
        
        return rr ('default/brainstorm.html')

# i must remove the hidden input
def comments (request , xid):
    if 'comment' in request.POST:
        com = request.POST['comment']
        cemail = request.POST['email']
        cstorm  = storm.objects.get (id = xid)
        newcom = comment (comment = com , storm = cstorm , email = cemail)
        newcom.save ()
        return rr ('default/brainstorm.html')
        
    else:
        t = get_template ('comment.html')
        comments = comment.objects.filter (storm = storm.objects.get (id = int (xid)))
        content = t.render (Context ({"comments" : comments}))
        cforms = comment_form (initial = {'storm' : xid})
        return rr ('index_1.html' , {"content" : content + cforms.as_complete_table () })


def new_cat (request):
    if 'title' in request.POST:
        cat = category (title = request.POST['title'] , published = False )
        cat.save ()
        return rr ('index_1.html' , {"content" : _('Your desire category was saved , we look at it and publish it as soon as possible.')})
    else:
        return rr  ('default/brainstorm.html')
