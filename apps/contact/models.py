# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) <17 may 2010>  Mohammad Hassanzadeh <hassanzadeh.mohammad@gmail.com>
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

# Create your models here.

class category (models.Model):
    """
         Entry class that hold category for contact.
    """
    title = models.CharField(max_length=20 , verbose_name=_("Title"))
    slug = models.SlugField (max_length=20 , verbose_name=_("Slug") , help_text = _("This field will fill automaticly by title field."))
    published = models.BooleanField (verbose_name = _("Publish ?") )
    category_order = models.IntegerField ( verbose_name = _("Order's"))
    description = models.TextField (verbose_name = _("Discription's"))
    def __unicode__ (self):
        return self.title
    def get_absolute_url (self):
        return "/contact/category/%s" % self.slug
    
class contact (models.Model):
    """
         Entry class that hold Contact information and viewing config.
    """
    #This part holding Necessary information
    name = models.CharField(max_length=20 , verbose_name=_("Name"))
    slug = models.SlugField (max_length=20 , verbose_name=_("Slug") , help_text = _("This field will fill automaticly by Name field."))
    published = models.BooleanField (verbose_name = _("Publish ?") )
    contact_order = models.IntegerField ( verbose_name = _("Order's"))
    category_id = models.ForeignKey(category)
    author = models.ForeignKey ("auth.User" , editable = True , verbose_name = _("Author"))
    
    #This part holding Optional information
    contact_position = models.CharField(max_length=20 , verbose_name=_("Contact's Position"))
    contact_position_flag = models.BooleanField (verbose_name = _("Contact's Position") )

    email = models.EmailField(verbose_name=_("E-mail Address"))
    email_flag = models.BooleanField(verbose_name=_("E-mail Address"))
    
    street_address = models.CharField(max_length=120 , verbose_name=_("Street Address"))
    street_address_flag = models.BooleanField(verbose_name=_("Street Address"))
    
    town = models.CharField(max_length= 30 , verbose_name=_("Town/Suburb"))
    town_flag = models.BooleanField( verbose_name=_("Town/Suburb"))
    
    state = models.CharField( max_length = 30 , verbose_name = _("State/County"))
    state_flag = models.BooleanField(verbose_name = _("State/County"))
    
    postalcode = models.CharField(max_length = 10 , verbose_name = _("Postalcode/Zip"))
    postalcode_flag = models.BooleanField(verbose_name = _("Postalcode/Zip"))
    
    tell = models.CharField(max_length = 15 ,verbose_name = _("Telephone"))
    tell_flag = models.BooleanField(verbose_name = _("Telephone"))
    
    cell = models.CharField(max_length = 15 ,verbose_name = _("Cell Phone"))
    cell_flag = models.BooleanField(verbose_name = _("Cell Phone"))
    
    fax = models.CharField(max_length = 15 ,verbose_name = _("Fax"))
    fax_flag = models.BooleanField(verbose_name = _("Fax"))
    
    weburl = models.URLField(verify_exists=True, max_length=200, verbose_name = _("Web Site URL's"))
    weburl_flag = models.BooleanField(verbose_name = _("Web Site URL's"))
    
    miscellaneous = models.TextField ( verbose_name = _("Miscellaneous Information"))
    miscellaneous_flag = models.BooleanField(verbose_name = _("Miscellaneous Information"))
    
    def __unicode__ (self):
        return self.name
    def get_absolute_url (self):
        return "/contact/%s" % self.slug
    
    
    