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
from django.template import Template


class Widget(dict):
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

    def get_html(self):
        if self.template:
            return get_template(self.template)
        else:
            if self.html:
                return Template(self.html)
            raise ValueError("'html' property should provide some HTML code")

    def render(self):
        pass

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

    @classmethod
    def load(cls, data):
        obj = cls().from_dict(data)
        return obj
