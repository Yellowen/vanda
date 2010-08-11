from django.shortcuts import render_to_response as rtr
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django import forms

from dina.log import Logger
from dina.conf.base import ConfigBase



def conf_view (req, appname):
    logger = Logger ("conf_view")
    logger.info ("APP name : %s" % appname)
    app_models = ContentType.objects.filter(app_label="appname")
    conf_models = list ()
    for i in app_models:
        if isinstance (i, ConfigBase):
            meta = type ("Meta" , () , {"model": i})
            formcls = type ("form_%s" % i , (forms.Form,) , {"Meta": meta})
            form = formcls ()
            logger.info ("Form : %s" % form)
            conf_models.append ((i.__name__, form))
            

    return HttpResponse ("OK")
