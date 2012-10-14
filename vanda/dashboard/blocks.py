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
from django.template.loader import get_template
from django.template import Template


class Block(object):
    """
    Block main class.
    """

    _widgets = {}

    template = None
    html = ""

    def get_html(self):
        if self.template:
            return get_template(self.template)
        else:
            if self.html:
                return Template(self.html)
            raise ValueError("'html' property should provide some HTML code")

    def __init__(self, dashboard, **options):
        self.dashboard = dashboard

    def render(self):
        """
        Render the block html code using widgets htmls.
        """
        return self.html.render()

    def add_widget(self, widget):
        # check for unique hash or something
        # we need this to add more than a Widget
        # instance in a block
        if not widget.name in self._widgets:
            self._widgets[widget.name]


class HorizontalBar(Block):
    pass


class WidgetArea(Block):
    pass


class SideBar(Block):
    pass
