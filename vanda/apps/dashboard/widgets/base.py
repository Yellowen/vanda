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
import json

from django.template.loader import get_template
from django.template import Template, Context
from django.conf.urls import patterns, url
from django.http import HttpResponse


class Widget(object):
    """
    Base class for all widgets.
    """
    title = ""
    name = ""

    #: Wheather show by default or not
    display = True

    #: Template file
    template = None

    #:
    html = ""

    dashboard = None
    _request = None

    @property
    def url_patterns(self):
        return []

    @property
    def urls(self):
        """
        Url dispatcher property.
        """
        url_patterns = self.url_patterns
        url_patterns.extend([
            url(r'^$', self.widget_html),
            ])
        urlpatterns = patterns('',
                               *url_patterns)
        return urlpatterns

    def set_dashboard_instance(self, dashboard):
        self.dashboard = dashboard

    def get_html(self):
        if self.template:
            return get_template(self.template)
        else:
            if self.html:
                return Template(self.html)
            return Template()

    def render(self):
        """
        Render the widget html code using widgets htmls.
        """
        html = self.get_html()
        return html.render(Context({"self": self}))

    def from_json(self, jsonstr):
        self.from_dict(json.loads(jsonstr))

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"title": self.title,
                "name": self.name,
                "display": self.display}

    def from_dict(self, dict_):
        for i in dict_:
            setattr(self, i, dict_[i])

    def get_element_id(self):
        if hasattr(self, "css_id"):
            if self.css_id:
                return self.css_id
        return "id_%s" % self.name

    def widget_html(self, request):
        self._request = request
        html = self.get_html()
        return HttpResponse(html.render(Context({"self": self})))

    @property
    def request(self):
        if self._request:
            return self._request
        elif self.dashboard:
            return self.dashboard.request

    @classmethod
    def load(cls, data):
        obj = cls().from_json(data)
        return obj
