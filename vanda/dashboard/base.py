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
from django.utils.translation import ugettext as _

import dashboard.blocks
from dashboard.widgets import Widget
from dashboard.models import UserDashboard


class Dashboard(object):
    _default_config = {
        "blocks": {"header": {"title": _("header"),
                                "class": "HorizontalBar"},
                     "aside": {"title": _("site bar"),
                               "class": "SideBar"},
                     "body": {"title": _("Dashboard"),
                              "class": "WidgetArea"},
                     "footer": {"title": _("footer"),
                                "class": "HorizontalBar"}}
        }

    _widgets = {}
    _widgets_types = {}
    _blocks = {}

    def __init__(self, options=_default_config):
        """
        Initializing the Dashboard.
        """
        for block in options["blocks"]:
            class_name = options["blocks"][block].get("class",
                                                      "WidgetArea")
            if hasattr(dashboard.blocks, class_name):
                klass = getattr(dashboard.blocks, class_name)
            else:
                raise ImportError("can't import '%s' from blocks")

            obj = klass(self, **options["blocks"][block])
            setattr(self, block, obj)
            self._blocks[block] = obj

    def register(self, widget):
        """
        Register the widget to dashboard widgets list.
        """
        if not isinstance(widget, Widget):
            raise TypeError("'widget' should be a 'Widget' Instance")

        if widget.name and widget.name not in self._widgets:
            self._widgets[widget.name] = widget
        else:
            return

        if not widget.__class__.__name__ in self._widgets_types:
            self._widgets_types[widget.__class__.__name__] = widget.__class__

    def load_config(self, config):
        blocks = config.get("blocks", {})

        for block in blocks:
            if block in self._blocks:
                # configure the corresponding block using configuration
                # string
                for widget_data in blocks[block]:
                    # Widget data is like (widget_type, widget_pickled_data)
                    widget_type = widget_data[0]

                    if widget_type in self._widgets_types:
                        widget = WidgetClass.load(widget_data[1])
                    else:
                        raise self.WidgetClassNotFound(
                            "No widget class '%s'." % widget_type.__name__)

                    self._blocks[block].add_widget(widget)

    def load_user_data(self, user):
        """
        Load the user's dashboard configuraion from database.
        """
        self.user_config = UserDashboard.get_data(user)
        if self.user_config:
            self.load_config(self.user_config)
        else:
            self.load_config({})

    class WidgetClassNotFound(Exception):
        pass


dashboard = Dashboard()
