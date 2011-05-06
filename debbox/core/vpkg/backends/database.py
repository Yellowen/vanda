# -----------------------------------------------------------------------------
#    VPKG - Vanda Package manager
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

from debbox.core.vpkg.models import Application


class Backend(object):
    """
    VPKG discovery backend class for database.
    """

    def __init__(self, *args, **kwargs):
        if "model" in kwargs:
            self.model = kwargs["model"]
        else:
            self.model = Application

    def installed_application(self):
        """
        Return a list of installed applications.
        """
        apps = self.model.objects.all()
        if apps:
            return [i.app for i in apps]
        else:
            return []
