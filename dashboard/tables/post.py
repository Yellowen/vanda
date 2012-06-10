# ---------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011-2012 Some Hackers In Town
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
# ---------------------------------------------------------------------------

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from dtable import ChangeTable, Field, Button
from ultra_blog.models import Post
from ultra_blog.base import post_types as PT


class PostsChangeTable(ChangeTable):
    name = "posts"
    template = "ublog/dashboard/posts.html"
    manager = Post.objects
    query_dict = {}

    fields = [
        Field("id", _("ID"), width=20, sortable=True),
        Field("title_link", _("Title"), width=200, sortable=True),
        Field("slug", _("Slug"), width=200),
        Field("site", _("Site"), width=200),
        Field("publish", _("Publish"), width=70),
        Field("comments_count", _("Comments"), width=70),
        Field("post_type_link", _("Type"), width=70),

        ]
    queryset_fields = ["id", "title_link", "slug", "site", "publish",
                       "comments_count", "post_type_link"]

    single_select = False
    resizable = True
    current_page = 1
    per_page = 10

    extra_context = {}

    title = _("Posts")

    buttons = [
        Button(_("Delete"), ["delete-post", []]),
        ]

    def _get_queryset_parameters(self, request):
        """
        Prepare a parameter dictionary for using in filter
        method of model Manger.
        """
        domain = request.get_host()
        try:
            from django.contrib.sites.models import Site

            site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            raise ValueError("Invalid domain name.")

        self.query_dict.update({"site": site})
        return self.query_dict

    def title_link(self, obj):
        """
        Generate the edit link.
        """
        return "<a href='%s'>%s</a>" % (reverse("edit-post", args=[obj.id]),
                                        obj.title)

    def post_type_link(self, obj):
        verbose_name = PT.get_type(obj.post_type_name).verbose_name
        return "<a href='%s'>%s</a>" % (reverse("edit-post-type",
                                                args=[obj.post_type_name,
                                                      obj.id]),
                                        verbose_name)


posts = PostsChangeTable()
