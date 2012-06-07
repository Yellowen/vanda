# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
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

import json

from django.template.loader import render_to_string as rs
from django.template import RequestContext


class Field(object):
    display = None
    name = None
    width = 50
    sortable = False
    align = "left"

    def __init__(self, name=None, display=None):
        self.name = name
        self.display = display

    def get_dict(self):
        return {"display": self.display,
                "name": self.name,
                "width": self.width,
                "sortable": self.sortable,
                "align": self.align,
                }


class ChangeTable(object):

    template = "ublog/dashboard/change_table.html"
    model = None
    manager = None
    fields = []

    css = ["css/blog/my/flexigrid.pack.css", ]
    js = ["js/my/flexigrid.pack.js", ]
    table_id = "grid"
    width = 700
    height = 400

    single_select = True
    resizable = False

    url = None
    title = "Grid"

    def __init__(self, request):
        method = request.method
        self.request = request

        self.query = request.GET
        if method == "POST":
            self.query = request.POST

        self.current_page = 1
        if "page" in self.query:
            self.current_page = self.query["page"]

        self.per_page = 10
        if "rp" in self.query:
            self.per_page = self.query["rp"]

    def _prepare_context(self):
        if not self.url:
            raise ValueError("'url' property should not be 'None'")

        result = []
        if self.manager:
            if self.query_dict:
                result = self.manager.filter(**query_dict)
            else:
                result = self.manager.all()
        elif self.model:
            if self.query_dict:
                result = self.model.objects.filter(**query_dict)
            else:
                result = self.model.objects.all()
        else:
            raise ValueError(
                "one of the 'model' or 'manager' properties should fill.")

        fields = []
        append = fields.append
        for field in self.fields:
            field_obj = None
            if isinstance(field, basestring):
                field_obj = Field(field.lower(), field.Capital())
            append(field_obj.get_dict())

        a = {"width": self.width,
             "height": self.height,
             "url": self.url,
             "title": self.title,
             "resizable": self.resizable,
             "single_select": self.single_select,
             "table_id": self.table_id,
             "scripts": self.js,
             "styles": self.css,
             "fields": json.dumps(fields),
             }
        return a

    def urls(self):
        """
        url dispatcher
        """
        from django.conf.urls.defaults import patterns


        urlpatterns = patterns('',
                               (r'^$', self.render),
                               (r'jsonp/$', self.json_data),
                               )
        return urlpatterns

    def json_data(self, request):
        """
        return posts list as json.
        """

        from ultra_blog.models import Post

        req_data = ["id", "title", "slug", "publish",
                    "tags", "author.username", "datetime", "update_datetime",
                    "site", "post_type_name"]

        posts = Post.objects.all()
        data = {"page": 1,
                "rows": [{"id": i.id,
                          "cell": i.get_dict(req_data)} for i in posts],
                "total": posts.count()}
        result = json.dumps(data)
        return HttpResponse(result)

    def render_to_string(self):

        context = self._prepare_context()
        return rs(self.template, context,
                  context_instance=RequestContext(self.request))
