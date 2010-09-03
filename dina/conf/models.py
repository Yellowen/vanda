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


class Config (models.Model):
    """
    Dina config base class.

    Each configuration model should inherit from this class.
    so dina can find out that that model is a application model.
    """


    
    def save(self, *args, **kwargs):
        # A config model should contain only one record
        self.__class__.objects.all ().delete ()
        super (Config, self).save (**kwargs)
        
    class Meta:
        abstract = True
        
    class _config:
        pass





class GeneralConfiguration (Config):
    """
    General Configuration for Dina.
    """
    
    # Fields
    site_name =  models.CharField (max_length = 50, verbose_name=_("Site Name"), \
                                   help_text=_("Site Name is a name that show in the title srction."),\
                                   default=_("Dina Project"))
    
    # Methods
    def __unicode__ (self):
        return "%s" % (self.site_name)






