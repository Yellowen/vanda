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


class Menu(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('name'))
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")


class MenuItem(models.Model):
    title = models.CharField(max_length=60, verbose_name=_('title'))
    image = models.ImageField(upload_to="menuimage", null=True, \
                              blank=True, verbose_name=_('image'))
    parent = models.ForeignKey('self', blank=True, null=True, \
                               verbose_name=_("Menu parent"))
    hasparent = models.BooleanField(verbose_name=_("menu has parent"))
    menu = models.ForeignKey(Menu)
    url = models.CharField(max_length=100, verbose_name=_("Link URL"))
    order = models.IntegerField(verbose_name=_("Menu order's"))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Itams")
