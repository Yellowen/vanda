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


from django.db import models
from django.utils.translation import ugettext as _

from dina.cache import Template as template_cache
from dina.DPM.models import Template as DPM_template
# TODO: build a optional layout for each page.


# Lets keep this model as simple as we can (lowest relations)
# for making layout prepration faster.
class TemplateLayouts (models.Model):
    """
    The layout manager will store the default sections of each templates
    in this model.
    """

    Template = models.ForeignKey (DPM_template) 
    Section = models.CharField (max_length=50)
    Contents = models.ManyToManyField ('Content', blank=True ,null=True)


    def save (self, force_insert=False, force_update=False):
        self.Template = template_cache.template
        super(TemplateLayouts, self).save (force_insert, force_update)
    
    class Meta:
        unique_together = ("Template", "Section")

    
# Content model need to completely optimize for next version
# TODO: Find a better way to deal with contents
class Content (models.Model):
    """
    This model will hold the Contents that sections should load.
    """
    TYPE = [
        ( '0' , _("Application Tag")),
        ( '1' , _("Application View")),
        ( '2' , _("Dina Application Tag")),
        ]
    
    App = models.CharField (max_length=80)
    # Type field is temporary field it will remove as soon as we can
    # Find a better way to deal with 3 type of contents.
    # at this time i have just 3 type of contents in my mind
    #       0. apps tags
    #       1. apps views output
    #       2. apps dina tag
    # TODO: find a better way to deal with contents types
    Type = models.CharField (max_length=1)

    # Name field will hold the 0 and 2 type tag name like
    #    {% Name ... %}
    
    Name = models.CharField (max_length=100, choices=TYPE)

    # Params file hold that 0 and 2 type tag parameters like
    #     {% Name  param1 param2 .... %}
    # parameters in Params field seperate with '$:$' characters
    Params = models.CharField (max_length=256, null=True, blank=True)


    # {% load MduleName %}
    ModuleName = models.CharField (max_length=30)


    # TODO: add the params field to unique_together
    class Meta:
        unique_together = ("App", "Name")

