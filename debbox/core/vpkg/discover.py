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


class ApplicationDiscovery (object):
    """
    Discover the installed applications and the stuff about them like
    url patterns and settings attributes.
    """

    def __init__(self, backend):

        tmplist = backend.split("://")
        self.backend = tmplist[0]
        self.address = None
        if len(tmplist) > 1:
            self.address = tmplist[1]

    def installed_application(self):
        pass

