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
        if isinstance(priority, int):
            self.priority = priority
        else:
            if priority in PRIORITY.keys():
                self.priority = PRIORITY[priority]
            else:
                raise self.InvalidPriority()

    def generator(self, lst):
        list_ = lst
        if isinstance(lst, str):
            list_ = [lst, ]
        for element in list_:
            yield element

    def url_patterns(self):
        """
        This method should return a list of url pattern that vpkg should use
        one of then as the main url entry for the application.

        but why this method should return a list?
        because if the first url already exists vpkg will use the next one
        application with higher priority will replace the exists url entry.

        each element of the returning list should be a dict that its keys
        will be the url pattern and its value will be the corresponding
        action it a value left None vpkg will automatically replace the
        action of that url pattern with `include('package.urls')`.

        if a urlpattern from an element already registered in vpkg, then
        vpkg replace the already registered pattern by the new one if current
        application have a higher priority otherwise vpkg will look for the
        same pattern in the next element dict and try to register that.

        so returning list should be like::

        [{'^some url pattern': None,  # will replace by include('package.urls')
        '^some other url': VIEW_FUNCTION},
        {'^alternative url pattern': None,
        '^some alter url': VIEW_FUNCTION}
        ]
        """
        pass

    class InvalidPriority (Exception):
        """
        the string that passed as priority is not valid.
        """
        pass
