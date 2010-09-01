from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.contrib import admin
from dina.log import Logger
from dina.conf.base import ConfigBase
from apps.testapp.models import config 

        

def conf_view (req, appname):
    logger = Logger ("conf_view")
    logger.info ("APP name : %s" % appname)
    app_models = ContentType.objects.filter(app_label=appname)
    conf_models = list ()
    form = None
    for i in app_models:

        if hasattr (i.model_class(), "_config"):
            form = admin.ModelAdmin (i.model_class(), admin.site)
            form.add_form_template = 'admin/dina/change_config.html'
            form.change_form_template = 'admin/dina/change_config.html'
            conf_models.append (i.model_class())
    if len (conf_models) > 1:
        raise "conf_models has more that one element"
    else:
        try:
            obj = conf_models[0].objects.all ()[0]
            return form.change_view (req, admin.util.quote(str(obj.pk)), )
        except IndexError:
            return form.add_view (req,  form_url='/admin/')
    
    
