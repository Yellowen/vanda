from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from dina.DPM.models import Template
from django.conf import settings


def MediaServ (request ,  path):
    current = Template.objects.Current ()
    i = 0
    mtype = 'plain/text'
    if path[-4:] in ['.jpg' , '.png']:
        mtype = 'image/*'
    # TODO: search in the TEMPLATE_DIRS for the statics files , not in the first element only
    fd = open (settings.TEMPLATE_DIRS[0] + "/" + current + '/media/' + path ,  'r''')
    buf = fd. read ()
    fd.close ()
    return HttpResponse (buf , mimetype=mtype)
        


