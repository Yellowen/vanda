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
import collections

from django.utils.translation import ugettext as _
from django.conf import settings
from django.conf.urls import patterns, url, include

from vanda.apps.dashboard import blocks as BLOCKS
from vanda.apps.dashboard.widgets import Widget
from vanda.apps.dashboard.models import UserDashboard


class JDict(dict):

    def to_dict(self):
        data = {}
        for key in self:
            data.update({key: self[key].to_dict()})
        return data


class Dashboard(object):
    _default_config = {
        "blocks": {"header": {"title": _("header"),
                              "class": "HorizontalBar"},
                   "aside": {"title": _("site bar"),
                             "class": "SideBar"},
                   "body": {"title": _("Dashboard"),
                            "class": "WidgetArea"},
                   "footer": {"title": _("footer"),
                              "class": "HorizontalBar"}},
        "css": [],
        "js": [],
    }

    _widgets = JDict()
    _widgets_types = {}
    _blocks = JDict()
    _css_widgets = set()
    _js = set()
    _css = set()
    _js_blocks_classes = set()
    _js_widgets_classes = set()
    _pre_js = set()

    _css_blocks = set()

    _json_blocks = {}
    _json_widgets = {}

    def __init__(self, options=_default_config):
        """
        Initializing the Dashboard.
        """
        if hasattr(settings, "DASHBOARD_CONFIG"):
            options = getattr(settings, "DASHBOARD_CONFIG")

        self._js_path = options.get("js_path",
                                    settings.MEDIA_URL).rstrip("/")
        self._css_path = options.get("css_path",
                                     settings.MEDIA_URL).rstrip("/")

        # Setup the global styles and scripts.
        styles = options.get("css", [])
        if styles:
            [self._css.add(i) for i in styles]

        scripts = options.get("js", [])
        if scripts:
            self._add_scripts(scripts, self)

        blocksclass = type("BlockList", (object, ), {})
        blocksobj = blocksclass()

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
            setattr(blocksobj, block, obj)
            self._blocks[block] = obj

            # Prepare javascript codes
            self._json_blocks[block] = {"id": obj.get_element_id(),
                                        "type": obj.__class__.__name__}

            self._js_blocks_classes.add(
                        "%s/blocks/%s.js" % (self._js_path,
                                             obj.__class__.__name__.lower()))

            # Preparing Csses
            self._css_blocks.add(
                "%s/blocks/%s.css" % (self._css_path,
                                      block.lower()))

            # Retrieve css and js addresses and add the to global styles
            # and scripts collection -----------------------------------
            if hasattr(obj, "js") and obj.js:
                self._add_scripts(obj.js, obj)

            # -----------------------------------------------------------

        setattr(self, "blocks", blocksobj)

    @property
    def urls(self):
        """
        Url dispatcher property.
        """
        urls_list = [
            url("^$", self.index,
                name="dashboard-index"),
            url("^js/dashboard.js$", self.js_lib,
                name="dashboard-js"),
            url("^js/initialize.js$", self.js_init,
                name="dashboard-init-js"),
        ]
        append = urls_list.append

        for widget in self._widgets:
            append(url(r'^widgets/%s/' % self._widgets[widget].name,
                       include(self._widgets[widget].urls),
                       name="%s-widget" % self._widgets[widget].name))

        urlpatterns = patterns('', *urls_list)
        return urlpatterns

    def register(self, widget):
        """
        Register the widget to dashboard widgets list.
        """
        widget.set_dashboard_instance(self)
        
        if not isinstance(widget, Widget):
            raise TypeError("'widget' should be a 'Widget' Instance")

        if widget.name and widget.name not in self._widgets:
            from django.core.urlresolvers import reverse

            self._widgets[widget.name] = widget
            self._json_widgets[widget.name] = {"id": widget.get_element_id(),
                                               "type": widget.__class__.__name__}
            self._js_widgets_classes.add(
                "%s/widgets/%s.js" % (self._js_path,
                                     widget.__class__.__name__.lower()))
        else:
            return

        if not widget.__class__.__name__ in self._widgets_types:
            self._widgets_types[widget.__class__.__name__] = widget.__class__

        self._css_widgets.add(
            "%s/widgets/%s.css" % (self._css_path,
                                   widget.name.lower()))
        if hasattr(widget, "pre_js"):
            if isinstance(widget.pre_js, basestring):
                self._pre_js.add(widget.pre_js)
            elif isinstance(widget.pre_js, collections.Iterable):
                map(lambda x: self._pre_js.add(x), widget.pre_js)
            else:
                raise ValueError("'pre_js' should be a list or string on '%s'" % \
                                 widget.__class__.__name__)

        if hasattr(widget, "js") and widget.js:
            self._add_scripts(widget.js, widget)

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
                        widget.set_dashboard_instance(self)
                    else:
                        raise self.WidgetClassNotFound(
                            "No widget class '%s'." % widget_type.__name__)

                    self._blocks[block].add_widget(widget)

    def save_config(self):
        """
        Save dashboard data in json format.
        """
        import json
        data = {"block": self._blocks.to_dict(),
                "widgets": self._widgets.to_dict()}

        print "data >>>> ", data
        return json.dumps(data)

    def add_widget_to(self, blockname, widget):
        '''
        Add a widget to a block.
        '''
        if widget.name in self._widgets:
            registered_widget = self._widgets[widget.name]
        else:
            raise ValueError("Given widget is not registered in dashboard")

        self._blocks[blockname].add_widget(registered_widget)
        self._json_widgets[registered_widget.name]["block"] = blockname

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
                __import__("%s.widgetset" % app,
                           globals(),
                           locals(),
                           ["widgetset", ], -1)
            except ImportError:
                pass

    def js_blocks_classes(self):
        return self._js_blocks_classes

    def js_widgets_classes(self):
        return self._js_widgets_classes

    def pre_js(self):
        return self._pre_js

    def styles(self):
        return set(list(self._css_blocks) + list(self._css_widgets) + \
                   list(self._css))

    def scripts(self):
        return self._js

    def _add_scripts(self, scripts, cls):
        if isinstance(scripts, basestring):
            self._js.add(scripts)
        elif isinstance(scripts, collections.Iterable):
            map(lambda x: self._js.add(x), scripts)
        else:
            raise ValueError(
                "Bad value for 'js' attirbute of '%s'" % cls.__class__.__name__)

    @property
    def widgets(self):
        return self._widgets

    # Views -----------------------------
    def index(self, request):
        """
        Dashboard index.
        """
        self.request = request
        from django.shortcuts import render_to_response as rr
        from django.contrib.auth.decorators import login_required
        from django.template import RequestContext

        @login_required
        def wrap(request):
            return rr("dashboard/index.html",
                      {},
                      context_instance=RequestContext(request))
        return wrap(request)

    def js_lib(self, request):
        """
        Return a javascript snippet to initialize dashboard js code.
        """
        from django.shortcuts import render_to_response as rr
        from django.contrib.auth.decorators import login_required
        from django.template import RequestContext

        @login_required
        def wrap(request):
            return rr("dashboard/js/dashboard.js",
                      mimetype="application/javascript",
                      context_instance=RequestContext(request))

        return wrap(request)

    def js_init(self, request):
        """
        Return a javascript snippet to initialize dashboard js code.
        """
        import json
        from django.shortcuts import render_to_response as rr
        from django.contrib.auth.decorators import login_required
        from django.template import RequestContext

        @login_required
        def wrap(request):
            return rr("dashboard/js/init.js",
                      {"blocks": json.dumps(self._json_blocks),
                       "widgets": json.dumps(self._json_widgets)},
                      mimetype="application/javascript",
                      context_instance=RequestContext(request))

        return wrap(request)
        
    class WidgetClassNotFound(Exception):
        pass


dashboard = Dashboard()
