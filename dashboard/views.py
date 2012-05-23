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

from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.comments.models import Comment

from forms import QMicroPostForm, QNewPostForm


@staff_member_required
def index(request):
    """
    Dashboard index.
    """
    micro_form = QMicroPostForm()
    post_form = QNewPostForm(request)
    last_comments = Comment.objects.filter(site__domain=request.META["HTTP_HOST"])[:10]
    return rr("ublog/dashboard/index.html",
              {"micro_form": micro_form,
               "post_form": post_form,
               "comments": last_comments},
              context_instance=RequestContext(request))
