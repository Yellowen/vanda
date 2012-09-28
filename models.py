# -----------------------------------------------------------------------------
#    Vanda dashbord - Dashboard application of Vanda platform
#    Copyright (C) 2012  Sameer Rahmani <lxsameer@gnu.org>
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
import json

from django.db import models
from django.utils.translation import ugettext as _


class UserDashboard(models.Model):
    """
    Users dashboard data.
    """
    user = models.ForeignKey('auth.User', verbose_name=_("User"))
    last_update = models.DateTimeField(_("last update"),
                                       auto_now=True,
                                       auto_now_add=True)
    _data = models.TextField(_("data"))

    @property
    def data(self):
        return json.loads(self._profile_data)

    @data.setter
    def data(self, value):
        self._profile_data = json.dumps(value)
        return json.dumps(value)

    @classmethod
    def get_data(cls, user):
        try:
            obj = cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None

        return obj.data

    def __unicode__(self):
        return "%s's dashboard data" % self.user.username

    class Meta:
        verbose_name = _("dashboard data")
        verbose_name_plural = _("Dashboards data")
