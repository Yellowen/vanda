# -----------------------------------------------------------------------------
#    Vanda forum - forum application for vanda platform
#    Copyright (C) 2011 Sameer Rahmani <lxsameer@gnu.org>
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
# -----------------------------------------------------------------------------

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Forum category model
    """
    user = models.ForeignKey(User, editable=False,
                             verbose_name=_("User"))
    title = models.CharField(max_length=60,
                            verbose_name=_("Title"))
    slug = models.SlugField(verbose_name=_("Slug"))
    parent = models.ForeignKey('self', verbose_name=_("Parent"),
                               blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                     verbose_name=_('Date and Time'))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        # TODO: i should use current registered url used by vpkg
        # instead of hardcoding forum url
        return "/forum/category/%s" % self.slug

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _('Category')


class Post(models.Model):
    """
    Post model.
    """
    title = models.CharField(max_length=64,
                             verbose_name=_("Title"))
    slug = models.SlugField(verbose_name=_("Slug"))
    author = models.ForeignKey(User, editable=False,
                             verbose_name=_("Author"))
    Category = models.ForeignKey(Category, editable=False,
                             verbose_name=_("Category"))
    content = models.TextField(verbose_name=("Content"))

    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                     verbose_name=_('Date and Time'))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        # TODO: i should use current registered url used by vpkg
        # instead of hardcoding post url
        return "/forum/post/%s" % self.slug

    class Meta:
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')


class Setting(models.Model):
    """
    Forum setting Model.
    """
    active = models.BooleanField(default=False,
                                 verbose_name=_("Active"))
    anonymous_post = models.BooleanField(default=False,
                                 verbose_name=_("Anonymous Post"))
    pre_moderation = models.BooleanField(default=False,
                                 verbose_name=_("pre-moderation"))
    ppp = models.IntegerField(default=20,
                              verbose_name=_("Post Per Page"))

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name_plural = _("Settings")
        verbose_name = _('Setting')
