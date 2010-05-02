from django.http import Http404
from django.contrib.auth.decorators import login_required

from dina.DPM.models import Template
from django.conf import settings


def MediaServ (request):
    current = Template.objects.Current ()
    i = 0
    while 1:
        fd = open (settings.TEMPLATE_DIRS[i] + "/")
        


