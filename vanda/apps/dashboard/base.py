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
from django.conf import settings
from django.conf.urls import patterns, url, include

from vanda.apps.dashboard import blocks as BLOCKS
from vanda.apps.dashboard.widgets import Widget
from vanda.apps.dashboard.models import UserDashboard


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
        if hasattr(settings, "DASHBOARD_CONFIG"):
            options = getattr(settings, "DASHBOARD_CONFIG")

        for block in options["blocks"]:
            class_name = options["blocks"][block].get("class",
                                                      "WidgetArea")
            if "class" in options["blocks"][block]:
                del options["blocks"][block]["class"]

            if hasattr(BLOCKS, class_name):
                klass = getattr(BLOCKS, class_name)
            else:
                raise ImportError("can't import '%s' from blocks" % class_name)

            obj = klass(self, **options["blocks"][block])
            self._blocks[block] = obj

    @property
    def urls(self):
        """
        Url dispatcher property.
        """
        urls_list = [
            url("^$", self.index,
                name="dashboard-index"),
        ]
        append = urls_list.append

        for widget in self._widgets:
            append(url(r'^widget/%s/' % widget.name,
                       include(widget.urls)))

        urlpatterns = patterns('', *urls_list)
        return urlpatterns

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
        """
        Initilize the dashboard instance using give config dict.
        """
        blocks = config.get("blocks", {})

        for block in blocks:
            if block in self._blocks:
                # configure the corresponding block using configuration
                # string
                for widget_data in blocks[block]:
                    # Widget data is like (widget_type, widget_pickled_data)
                    widget_type = widget_data[0]

                    if widget_type in self._widgets_types:
                        widget = Widget.load(self._widgets_types[widget_type],
                                             widget_data[1])
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

    def auto_discovery(self):
        """
        Walk throught the installed apps and look for a widget module
        of package and import them.
        """
        for app in settings.INSTALLED_APPS:
            try:
                print ">>> 1111%s" % app
                m = __import__("%s.widgets" % app,
                           globals(),
                           locals(),
                           ["widgets"], -1)
                print ">>>>>> 22222", m
            except ImportError, e:
                print e

    def __getattr__(self, blockname):
        """
        Return the corresponding block object or actual attribute.
        """
        if blockname in self._blocks:
            return self._blocks[blockname]
        elif hasattr(self, blockname):
            return getattr(self, blockname)
        else:
            raise AttributeError("No such attribute '%s'" % blockname)

    # Views -----------------------------
    def index(self, request):
        """
        Dashboard index.
        """
        from django.shortcuts import render_to_response as rr
        from django.contrib.auth.decorators import login_required
        from django.template import RequestContext

        @login_required
        def wrap(request):
            return rr("dashboard/index.html",
                      {},
                      context_instance=RequestContext(request))
        return wrap(request)

    class WidgetClassNotFound(Exception):
        pass


dashboard = Dashboard()
