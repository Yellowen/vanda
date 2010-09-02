import sets
from django.shortcuts import render_to_response as rtr
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.utils.translation import ugettext as _

from dina.log import Logger



        

def conf_view (req, appname):
    logger = Logger ("conf_view")
    app_models = ContentType.objects.filter(app_label=appname)
    logger.info ("APP name : %s" % appname)
    conf_models = list ()
    form = None
    app_models = [i.model_class() for i in app_models]
    app_models_set = sets.Set(app_models)
    registry = sets.Set (admin.site._registry)
    if len ( app_models_set & registry) == 0:
        return rtr ("admin/dina/info.html", {"app_label": appname,\
                                             "msg": _("Warning: \"%s\" application does not provide a admin interface. (do not have a \"admin.py\")") % appname })
    for i in app_models:

        
        if hasattr (i, "_config"):
            logger.debug ("config model: %s" % i)
            form = admin.ModelAdmin (i, admin.site)
            form.add_form_template = 'admin/dina/change_config.html'
            form.change_form_template = 'admin/dina/change_config.html'
            conf_models.append (i)

    if  len (conf_models) != 1 :
        return rtr ("admin/dina/info.html", {"app_label": appname,\
                                             "msg": _("Warning: \"%s\" application does not provide a config model.") % appname })

    else:
        try:
            obj = conf_models[0].objects.all ()[0]
            return form.change_view (req, admin.util.quote(str(obj.pk)), )
        except IndexError:
            return form.add_view (req,  form_url='/admin/')
    
    
