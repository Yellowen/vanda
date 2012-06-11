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
from django.contrib.comments.models import Comment
from ultra_blog.base import post_types as PT


class CommentsChangeTable(ChangeTable):
    name = "comments"
    template = "ublog/dashboard/posts.html"
    model = Comment
    query_dict = {}

    fields = [
        Field("id", _("ID"), width=20, sortable=True),
        Field("is_public_edit_link", _("Public"), width=70),
        Field("comment_link", _("Comment"), width=400, sortable=True),
        Field("user_email", _("User Mail"), width=200, sortable=True),
        Field("site", _("Site"), width=100, sortable=True),
        Field("submit_date", _("Submit Date"), width=150),
        Field("ip_address", _("IP"), width=70),

        Field("is_removed", _("Removed"), width=70),
        ]
    queryset_fields = ["id", "is_public_edit_link", "comment_link", "user_email", "site",
                       "submit_date", "ip_address",
                       "is_removed"]

    wrap_cell = True

    single_select = False
    resizable = True
    current_page = 1
    per_page = 10

    monkey_patch = True

    extra_context = {}

    title = _("Comments")

    buttons = [
         Button(_("Delete"), ["delete-comment", []]),
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

    def comment_link(self, obj):
        """
        Generate the edit link.
        """
        
        #return "<a href='%s'>%s</a>" % (reverse("edit-post", args=[obj.id]),
        #                                obj.comment)
        return obj.comment

    def is_public_edit_link(self, obj):
        """
        Convert the is_public to a link for edition.
        """
        return "<a href='%s'>%s</a>" % (reverse("edit-comment-public", args=[obj.id]),
                                        obj.is_public)


comments = CommentsChangeTable()
