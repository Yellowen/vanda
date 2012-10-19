# -----------------------------------------------------------------------------
#    Vanda page application
#    Copyright (C) 2010-2012 Sameer Rahmani <lxsameer@gnu.org>
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
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from django.conf import settings


class Page(models.Model):
    """
    Page main model class
    """
    user = models.ForeignKey(User, editable=False,
                             verbose_name=_("User"))
    title = models.CharField(max_length=30,
                             verbose_name=_("Title"))
    slug = models.SlugField(max_length=30, unique=True,
                            verbose_name=_("Slug"))
    # IMPORTANT: content field will render as html
    content = models.TextField(verbose_name=_("Page content"))

    site = models.ForeignKey(Site, verbose_name=_("Site"))
    language = models.CharField(_("Language"),
                                max_length=4,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGES[0][0])

    publish = models.BooleanField(default=False,
                                  verbose_name=_("Publish"))

    menu = models.BooleanField(default=False,
                               verbose_name=_("Appear in navigation?"))

    weight = models.IntegerField(default=40, verbose_name=_("Weight"))
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                     verbose_name=_('Date and Time'))

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("page.views.show_page" % self.slug)

    class Meta:
        verbose_name_plural = _("Pages")
        verbose_name = _('Page')
        ordering = ['-weight']
