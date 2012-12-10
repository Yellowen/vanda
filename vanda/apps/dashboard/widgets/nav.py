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

from base import Widget


class MenuItem (object):

    def __init__(self, name, link="#", submenus=[]):
        self.name = name
        self.link = link
        self.menus = submenus

    def render(self):
        pass


class NavigationMenu (Widget):
    name = "navigation_menu"
    title = "Navigation"
    template = "dashboard/widgets/navigation_menu.html"

    #: You can simply use a dictionary like object to obtain menu items like::
    #:
    #: navigation_items = {"home" : "/",
    #:                     "pages": {"first page": "/first/page/",
    #:                               "second page": /2th/page/"}
    #:                    }
    #:
    #: You can use models to provide menu items too.
    navigation_dict = {}

    def get_items(self, navdict={}):
        if navdict:
            nav_dict = navdict
        else:
            nav_dict = self.navigation_dict

        items = []
        append = items.append
        for key in nav_dict:
            if isinstance(nav_dict[key], dict):
                append(MenuItem(name=key,
                                submenus=self.get_items(nav_dict[key])))
            else:
                append(MenuItem(name=key, link=nav_dict[key]))
        print "<<<<< ", items
        return items

    def to_dict(self):
        a = super(NavigationMenu, self).to_dict()
        a.update({"navigation_dict": self.navigation_dict})
        return a
