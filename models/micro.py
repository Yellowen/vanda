# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Some Hackers In Town
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
from django.contrib.admin.models import User
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site


class MicroPost(models.Model):
    """
    Micro post model.
    """

    content = models.TextField(_("What's in your mind?"))

    author = models.ForeignKey(User,
                               editable=False,
                               verbose_name=_("Author"))

    datetime = models.DateTimeField(auto_now_add=True, editable=False,
                                    verbose_name=_('Date and Time'))

    site = models.ForeignKey(Site, verbose_name=_("Site"),
                             null=True, blank=True)

    class Meta:
        app_label = "ultra_blog"
        ordering = ["-datetime"]
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')
