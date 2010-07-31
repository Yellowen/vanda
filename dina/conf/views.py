from django.shortcuts import render_to_response as rtr
from django.http import HttpResponse
from django.conf import settings

from dina.log import Logger

def conf_view (req, appname):
    logger = Logger ("conf_view")
    logger.info ("APP name : %s" % appname)
    return HttpResponse ("OK")
