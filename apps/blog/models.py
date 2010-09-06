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

# Create your models here.

class category (models.Model):
    title = models.CharField (max_lenght=250 , verbose_name=("Title"))
    slug = models.SlugField (max_length=100 , verbose_name=_("Slug"),help_text = _("This gield will fill automaticaly by title"))
    description = models.TextField()

    def __unicode__(self):
        return self.title

class post (models.Model):
    """
    Entry model that hold posts
    """
    title = models.CharField (max_length=250 , verbose_name=_("Title"))
    slug = models.SlugField (max_length=100 , verbose_name=_("Slug") , help_text = _("This field will fill automaticly by title field."))
    author = models.ForeignKey ("auth.User" , editable = False , verbose_name = _("Author"))
    datetime = models.DateTimeField (auto_now_add = True , editable=False , verbose_name = _('Date and Time'))
    text = models.TextField (verbose_name = _('Text'))
    
    def __unicode__ (self):
        return self.title
    def get_absolute_url (self):
        return "/blog/post/%s" % self.slug
    
    class Meta:
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')

