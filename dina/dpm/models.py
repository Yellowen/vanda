# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------

from django.db import models
from django.utils.translation import gettext as _


class Package (models.Model):
    """
    Base class for dpm packages.
    """
    sha1sum = models.SHA1Field(verbose_name=_("SHA1 checksum"))
    name = models.CharField(max_length=40, \
                            verbose_name=_("Name"))
    version = models.VersionField(verbose_name=_("Version"))
    section = models.CharField(max_length=20, verbose_name=_("Section"))
    priority = models.CharField(max_length=15, verbose_name=_("Priority"))
    maintainer = models.CharField(max_length=60, verbose_name=_("Maintainer"))
    uploaders = models.CharField(max_length=100, blank=True, null=True, \
                                 verbose_name=_("Uploaders"))
    homepage = models.UrlField(blank=True, null=True, \
                               verbose_name=_("Home Page"))

    sign = models.SignField(verbose_name=_("Sign"))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.pkg_name

    def pkg_name(self):
        return "%s_%s" % (self.name, self.version)

    class Meta:
        abstract = True
