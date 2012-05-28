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

import json

from django.shortcuts import render_to_response as rr
from django.template.loader import render_to_string as rs
from django.template import RequestContext
from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from forms import QMicroPostForm, QNewPostForm


@staff_member_required
def index(request):
    """
    Dashboard index.
    """
    micro_form = QMicroPostForm()
    post_form = QNewPostForm(request)
    last_comments = Comment.objects.filter(site__domain=request.get_host())[:10]
    return rr("ublog/dashboard/index.html",
              {"micro_form": micro_form,
               "post_form": post_form,
               "comments": last_comments},
              context_instance=RequestContext(request))


@staff_member_required
def micro_post(request):
    """
    Add a new micro post to database.
    """

    if request.method == "POST":
        domain = request.get_host()
        try:
            site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            raise Http404()

        # TODO: uncomment following code to authenticating against per user
        # subdomain.

        # profile = request.get_profile()
        # if profile.site.domain == site:

        from ultra_blog.models import MicroPost, Status

        try:
            status = Status.objects.get(id=int(request.POST["status"]))

        except Status.DoesNotExist:
            return HttpResponse(json.dumps({"status": 1,
                                            "msg": _("wrong status")}))

        mpost = MicroPost()
        mpost.author = request.user
        mpost.content = request.POST["message"]
        mpost.site = site
        mpost.save()

        return HttpResponse(json.dumps({"status": 0,
                                        "msg": _("Done")}))
    return HttpResponseForbidden()


@staff_member_required
def new_post(request):
    """
    Adding new post.
    """
    if request.method == "POST":

        domain = request.get_host()
        try:
            site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            raise Http404()

        # TODO: uncomment following code to authenticating against per user
        # subdomain.

        # profile = request.get_profile()
        # if profile.site.domain == site:

        from ultra_blog.models import Post, Category

        print ">>>", request.POST


@staff_member_required
def posts(request):
    """
    Posts index.
    """
    from ultra_blog.models import Post


    posts = Post.sites.all()
    content = rs("ublog/dashboard/grid.html",
                 {"posts": posts},
                 context_instance=RequestContext(request))

    return rr("ublog/dashboard/page.html",
              {"content": content},
              context_instance=RequestContext(request))
