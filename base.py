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

from django.http import HttpResponse
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

    template = "dtable.html"
    model = None
    manager = None

    fields = []
    queryset_fields = []

    css = ["css/blog/my/flexigrid.pack.css", ]
    js = ["js/my/flexigrid.pack.js", ]
    table_id = "grid"
    width = 700
    height = 400

    single_select = True
    resizable = False
    current_page = 1
    per_page = 10

    extra_context = {}

    url = None
    title = "Grid"

    urlpatterns = [
        (r'^$', render),
        (r'jsonp/$', json_data),
        ]

    def _prep_params(self, request):
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


        fields = []
        append = fields.append
        for field in self.fields:
            field_obj = None
            if isinstance(field, basestring):
                field_obj = Field(field.lower(), field.title())
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
             "rp": self.per_page,
             }
        return a

    def urls(self):
        """
        url dispatcher
        """
        from django.conf.urls.defaults import patterns

        urlpatterns = patterns('', *self.urlpatterns)
        return urlpatterns

    def json_data(self, request):
        """
        return posts list as json.
        """

        def end_check(end_index, counts):
            """
            Check for ending index overflow.
            """
            if end_index > counts:
                end_index = end_index - (end_index - counts)
            return end_index

        self._prep_params(request)

        result = []
        counts = 0

        start_index = self.current_page * self.per_page
        end_index = start_index + self.per_page

        if self.manager:
            if self.query_dict:
                counts = self.manager.filter(**query_dict).count()
                end_index = end_check(end_index, counts)
                result = self.manager.filter(**query_dict)[start_index:end_index]
            else:
                counts = self.manager.all().count()
                end_index = end_check(end_index, counts)
                result = self.manager.all()[start_index:end_index]
        elif self.model:
            if self.query_dict:
                counts = self.model.objects.filter(**query_dict).count()
                end_index = end_check(end_index, counts)
                result = self.model.objects.filter(**query_dict)[start_index:end_index]
            else:
                counts = self.model.objects.all().count()
                end_index = end_check(end_index, counts)
                result = self.model.objects.all()[start_index:end_index]
        else:
            raise ValueError(
                "one of the 'model' or 'manager' properties should fill.")

        data = self._jsonify_data(result, counts)
        return HttpResponse(data)

    def _jsonify_data(self, queryset, counts):
        """
        Return a suitable json data for flexitable.
        """
        a = {"page": self.current_page,
             "rows": [
                 {"id": i.id,
                  "cell": i.get_dict(self.queryset_fields)} for i in queryset],
             "total": counts}

        return json.dumps(a)

    def render(self):
        context = self._prepare_context()
        context.update(self.extra_context)
        return rs(self.template, context,
                  context_instance=RequestContext(self.request))
