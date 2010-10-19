# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------------

import sets

from django.shortcuts import render_to_response as rtr
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.utils.translation import ugettext as _

from dina.log import Logger

       

def conf_view (req, appname):
    """
    Configuration from view.
    """
    logger = Logger ("conf_view")

    # Get the models list for the appname application
    app_models = ContentType.objects.filter(app_label=appname)
    logger.debug ("APP name : %s" % appname)
    conf_models = list ()
    form = None
    
    # Build set from models list and site._registry, so we can
    # easily check for the applications that have a registerd ModelAdmin
    # those application that don't have a ModelAdmin did not have a Admin
    # interface
    app_models = [i.model_class() for i in app_models]
    app_models_set = sets.Set(app_models)
    registry = sets.Set (admin.site._registry)
    if len ( app_models_set & registry) == 0:
        return rtr ("admin/dina/info.html", {"app_label": appname,\
                                             "msg": _("Warning: \"%s\" application does not provide a admin interface. (do not have a \"admin.py\")") % appname })

    
    for i in app_models:

        # Check for _config subclass inside of model, only config classes
        # have one
        if hasattr (i, "ConfigAdmin"):
            logger.debug ("config model: %s" % i)

            # Change the defualt add and change view of generated ModelAdmin
            # to build a form from config model
            form = admin.ModelAdmin (i, admin.site)
            form.add_form_template = 'admin/dina/change_config.html'
            form.change_form_template = 'admin/dina/change_config.html'
            form.fieldsets = i.ConfigAdmin.fieldsets
            conf_models.append (i)


    # Each model must have just one config model
    if  len (conf_models) != 1 :
        return rtr ("admin/dina/info.html", {"app_label": appname,\
                                             "msg": _("Warning: \"%s\" application does not provide a config model.") % appname })
    else:
        try:
            # Load the change view with exists data
            obj = conf_models[0].objects.all ()[0]
            return form.change_view (req, admin.util.quote(str(obj.pk)), )
        except IndexError:
            # Load the new add view for first data entry
            return form.add_view (req)#, form_url='/admin/')
    
    
