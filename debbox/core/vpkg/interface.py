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

PRIORITY = {
    "low": 0,
    "normal": 50,
    "high": 100,
    }


class BaseApplication(object):
    """
    VPKG interface to Django applications.  Each Django app should implement
    this interface in its ``__init__.py`` with name of ``application``.
    """

    def __init__(self, priority):
        self.priority = priority

    def url_patterns(self):
        """
        This method should return a list of url pattern that vpkg should use
        one of then as the main url entry for the application.

        but why this method should return a list?
        because if the first url already exists vpkg will use the next one
        application with higher priority will replace the exists url entry.

        vpkg will include the urls.py inside the application package for
        selected url so urls entries should not end with `$`
        """
        pass
