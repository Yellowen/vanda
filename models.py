# -----------------------------------------------------------------------------
#    Vanda - Web development platform
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
from django.utils.translation import ugettext as _


class Country(models.Model):
    """
    This model stores the country names.
    """
    name = models.CharField(max_length=32, verbose_name=_("Name"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class State(models.Model):
    """
    This model stores the states of each country.
    """
    country = models.ForeignKey(Country, verbose_name=_("Country"))
    name = models.CharField(max_length=32, verbose_name=_("Name"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")


class City(models.Model):
    """
    This model stores the cities of each state.
    """
    state = models.ForeignKey(State, verbose_name=_("State"))
    name = models.CharField(max_length=32, verbose_name=_("Name"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("City")
