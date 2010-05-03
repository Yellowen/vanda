# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) $YEAR$  $AUTHOR$
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


class TemplateManager (models.Manager):
    """
    This manager will add to template model and provide some functions like:
    setActive : this function the a template as active (template in use)
    """
    
    
    def setActive (self):
        """
        Set a template as active and deactivate lastest active template.
        """
        
        print str (self.get_query_set ())
        pass


    def Current (self):
        """
        Return the current active themplate.
        """
      
        current = super(TemplateManager , self).get_query_set ().get (Active=True).Name
        return '%s/' % current
