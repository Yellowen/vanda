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

class section(models.Model):
    title = models.CharField (max_length=30 , verbose_name=_("Title") , help_text=_("Title will show as page <title> tag."))
    slug = models.SlugField (verbose_name=_("Slug") , help_text=_("This field will fill automaticly by title.") , unique=True)
    published = models.BooleanField (verbose_name=_("Publish ?"))
    description = models.TextField (verbose_name=_("Body") , help_text=_("HTML allowed."))
    image = models.ImageField (upload_to="page/sections/" , verbose_name=_("Section image's"))
    
    def __unicode__ (self):
        return self.title
    
    def get_absolute_url (self):
        return "/section/%s/" % self.slug

class category (models.Model):
    section = models.ForeignKey("section" , verbose_name=_("Section name"))
    title = models.CharField (max_length=30 , verbose_name=_("Title") , help_text=_("Title will show as page <title> tag."))
    slug = models.SlugField (verbose_name=_("Slug") , help_text=_("This field will fill automaticly by title.") , unique=True)
    published = models.BooleanField (verbose_name=_("Publish ?"))
    description = models.TextField (verbose_name=_("Body") , help_text=_("HTML allowed."))
    image = models.ImageField (upload_to="page/category/" , verbose_name=_("Category image's"))

    def __unicode__ (self):
        return  self.title

    def get_absolute_url (self):
        return "/category/%s/" % self.slug


class page (models.Model):
    category = models.ForeignKey ("category" , verbose_name=_("Category Name"))
    title = models.CharField (max_length=30 , verbose_name=_("Title") , help_text=_("Title will show as page <title> tag."))
    slug = models.SlugField (verbose_name=_("Slug") , help_text=_("This field will fill automaticly by title.") , unique=True)
    content = models.TextField (verbose_name=_("Body") , help_text=_("HTML allowed."))
    date = models.DateTimeField(db_index=True, auto_now_add=True)
    published = models.BooleanField (verbose_name=_("Publish ?"))
    home = models.BooleanField (verbose_name=_("Shall it be home page ?") , help_text=_("Only one page can be the home page at a time."))

    def __unicode__ (self):
        return self.title

    
    def get_absolute_url (self):
        return "/pages/%s/" % self.slug
