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
from django.template import Template, Context
from django.utils.translation import ugettext as _


class Block(object):
    """
    Block main class.
    """
    template = None
    html = ""
    order_matters = False

    _widget_list = []

    
    def __init__(self, dashboard, **options):
        """
        Initialize the block instance.
        """
        from vanda.apps.dashboard.base import JDict

        self.title = options.get("title", _("untitle"))
        self.css = options.get("css", None)
        self.js = options.get("js", None)
        self.order_matters = options.get("order_matters", False)

        self.dashboard = dashboard
        self._widgets = JDict()

    def get_html(self):
        if self.template:
            return get_template(self.template)
        else:
            if self.html:
                return Template(self.html)
            else:
                return Template()

    def render(self):
        """
        Render the block html code using widgets htmls.
        """
        html = self.get_html()
        return html.render(Context({"self": self}))

    def add_widget(self, widget):
        # check for unique hash or something
        # we need this to add more than a Widget
        # instance in a block

        if not widget.name in self._widgets:
            if self.order_matters:
                weight = 500
                if hasattr(widget, "weight"):
                    weight = widget.weight
                self._widget_list.append([weight, widget])
                self._widget_list.sort()
                self._widget_list.reverse()

            self._widgets[widget.name] = widget

    def to_dict(self):
        return self._widgets.to_dict()
    ##     """
    ##     Return a jsonable dictionary which contains block data.
    ##     """
    ##     data = {}
    ##     for widgetname in self._widgets:
    ##         data.update({widgetname: self._widgets[widgetname].to_dict()})

    ##     return data
    
    def widgets(self):
        """
        Return a list of block widgets.
        """
        if self.order_matters:
            return map(lambda x: x[1], self._widget_list)
        return self._widgets.values()

    def get_element_id(self):
        if hasattr(self, "css_id"):
            if self.css_id:
                return self.css_id
        return "id_%s" % self.title
