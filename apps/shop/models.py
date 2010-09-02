# -*- coding: utf-8 -*-
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
from django.contrib.auth.models import User

class shopCategories (models.Model):
    name  = models.CharField (verbose_name=_('Shop category title')max_length = 100)
    description = models.TextField(verbose_name=_('Shop category description'),null=True, blank=True)
    image = models.ImageField(verbose_name=_('Shop category image'),height_field=None, width_field=None,max_length="7000",upload_to="uploads/shop/")
    
    def __unicode__(self):
        return "%s" % self.name
        
class products(models.Mode):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100,null=True, blank=True)
    category = models.ForeignKey(shopCategories)
    
    class Meta:
        abstract = True
