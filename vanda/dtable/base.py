# -----------------------------------------------------------------------------
#    Dtable - data table application for Vanda platform
#    Copyright (C) 2012 Some Hackers In Town
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
from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class Field(object):
    """
    Represent a table field.
    """
    display = None
    name = None
    width = 50
    sortable = False
    align = "left"

    def __init__(self, name=None, display=None,
                 width=50, sortable=False, align="left"):
        self.name = name
        self.display = display
        self.width = width
        self.sortable = sortable
        self.align = align

    def get_dict(self):
        return {"display": self.display,
                "name": self.name,
                "width": self.width,
                "sortable": self.sortable,
                "align": self.align,
                }


class Button(object):
    """
    Represent a flexitable button.
    """

    def __init__(self, name, url, tooltip="", bclass="",
                 bimage=""):
        self.name = name
        self.id = "%s_id" % name.lower()

        # url must be a list that first index is the name of url
        # specified in url() function. and secend arg should be
        # a list or dictionary of posible arguments pass to reverse
        # function
        self.url = url
        self.tooltip = tooltip
        self.bclass = bclass
        self.bimage = bimage

    def __unicode__(self):
        result = "{"
        for i in ["name", "id", "url", "tooltip", "bclass",
                  "bimage"]:
            value = getattr(self, i)
            if value:
                if i == "url":
                    result = result + i + ": '" + reverse(
                        value[0],
                        args=value[1]) + "', "
                else:
                    result = result + i + ": '" + value + "', "

        return mark_safe(result + " onpress: do_command},")


class ChangeTable(object):
    """
    Base Class for all the change views.
    """
    name = ""
    template = "dtable.html"
    model = None
    manager = None
    query_dict = {}

    # Remember to use model with monkey patch not manager
    monkey_patch = False

    fields = []
    queryset_fields = []

    buttons = []
    button_separator = True

    css = ["css/flexigrid.pack.css", ]
    js = ["js/flexigrid.pack.js", ]
    wrap_cell = False
    table_id = "grid"
    width = mark_safe("\"auto\"")
    height = mark_safe("\"auto\"")

    single_select = True
    resizable = False
    current_page = 1
    per_page = 10

    extra_context = {}

    url = None
    title = "Grid"

    urlpatterns = []

    def _prep_params(self, request):
        method = request.method
        self.request = request

        self.method = request.GET
        if method == "POST":
            self.method = request.POST

        self.current_page = 1
        if "page" in self.method:
            self.current_page = self.method["page"]

        self.per_page = 10
        if "rp" in self.method:
            self.per_page = self.method["rp"]

    def _prepare_context(self):
        """
        Prepare the context for rendering template.
        """

        fields = []
        append = fields.append
        for field in self.fields:
            field_obj = None
            if isinstance(field, basestring):
                field_obj = Field(field.lower(), field.title())
            else:
                field_obj = field
            append(field_obj.get_dict())

        ## buttons = []
        ## append = buttons.append
        ## for button in self.buttons:
        ##     bclass = "btn"
        ##     if len(button) > 1:
        ##         bclass = button[1]
        ##     append([button[0], bclass])

        a = {"width": self.width,
             "height": self.height,
             "url": reverse("%s-jsonp" % self.name, args=[]),
             #"jsonpname": "%s-jsonp" % self.name,
             "title": self.title,
             "resizable": str(self.resizable).lower(),
             "single_select": str(self.single_select).lower(),
             "table_id": self.table_id,
             "scripts": self.js,
             "styles": self.css,
             "fields": mark_safe(json.dumps(fields)),
             "buttons": self.buttons,
             "nowrap": str(not self.wrap_cell).lower(),
             "rp": self.per_page,
             }
        return a

    @property
    def urls(self):
        """
        url dispatcher
        """
        ## def wrap(view, cacheable=False):
        ##     def wrapper(*args, **kwargs):
        ##         return self.views(view)(*args, **kwargs)
        ##     return update_wrapper(wrapper, view)

        from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns('',
                               url(r'^$', self.render, name=self.name),
                               url(r'jsonp/$', self.json_data,
                                   name=self.name + "-jsonp"),
                               )
        return urlpatterns + self.urlpatterns

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

        query = ""
        if "sortname" in self.method:
            if self.method["sortname"]:
                query = self.method["sortname"]

        if "sortorder" in self.method:
            if self.method["sortorder"] == "desc":
                query = "-%s" % query

        result = []
        counts = 0

        start_index = (int(self.current_page) - 1) * int(self.per_page)
        end_index = start_index + int(self.per_page)

        query_dict = self._get_queryset_parameters(request)

        if self.monkey_patch:
            from models import DTModel
            func = DTModel.get_class_dict

            setattr(self.model, "get_dict", DTModel.get_class_dict)

        if self.manager:
            if query_dict:
                counts = self.manager.filter(**query_dict).count()
                end_index = end_check(end_index, counts)
                result = self.manager.filter(**query_dict).order_by(query)[start_index:end_index]

            else:
                counts = self.manager.all().count()
                end_index = end_check(end_index, counts)
                result = self.manager.all().order_by(query)[start_index:end_index]

        elif self.model:
            if query_dict:
                counts = self.model.objects.filter(**query_dict).count()
                end_index = end_check(end_index, counts)
                print "<<<<", query_dict, query
                result = self.model.objects.filter(**query_dict).order_by(query)[start_index:end_index]

            else:
                counts = self.model.objects.all().count()
                end_index = end_check(end_index, counts)
                result = self.model.objects.all().order_by(query)[start_index:end_index]
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
                  "cell": i.get_dict(self.queryset_fields,
                                     self)} for i in queryset],
             "total": counts}

        return json.dumps(a)

    def render(self, request):
        """
        Render the final template.
        """
        context = self._prepare_context()
        context.update(self.extra_context)
        return rr(self.template, context,
                  context_instance=RequestContext(request))

    def _get_queryset_parameters(self, request):
        """
        Prepare a parameter dictionary for using in filter
        method of model Manger.
        """
        return self.query_dict
