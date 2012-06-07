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
from django.http import (HttpResponseForbidden, Http404, HttpResponse,
                         HttpResponseRedirect)
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from ultra_blog.base import post_types as PT
from forms import QMicroPostForm, QNewPostForm


@staff_member_required
def index(request):
    """
    Dashboard index.
    """

    # Create the necessary forms
    micro_form = QMicroPostForm()
    post_form = QNewPostForm(request)

    last_comments = Comment.objects.filter(
        site__domain=request.get_host())[:10]

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
    def on_invalid_form(form):
            rendered_form = rs("ublog/dashboard/forms.html",
                               {"action":
                                reverse("ultra_blog.dashboard.views.new_post",
                                        args=[]),
                                "form": form},
                               context_instance=RequestContext(request))

            return rr("ublog/dashboard/page.html",
                      {"content": rendered_form,
                       "title": _("New Post")},
                      context_instance=RequestContext(request))

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

        new_post_form = QNewPostForm(request, request.POST)
        if new_post_form.is_valid():

            from ultra_blog.models import Post, Category

            prev_data = new_post_form.cleaned_data

            try:
                post = Post.objects.get(slug=prev_data["slug"])
                new_post_form._errors = {"slug":
                                         _("This slug already exists.")}
                return on_invalid_form(new_post_form)

            except Post.DoesNotExist:
                pass


            post_form = PT.get_form(prev_data["post_type"])
            request.session["new_post_data"] = prev_data
            request.session["new_post_type_form"] = post_form

            rendered_form = rs("ublog/dashboard/forms.html",
                               {"action":
                                reverse("ultra_blog.dashboard.views.save_post",
                                        args=[]),
                                "form": post_form},
                               context_instance=RequestContext(request))

            return rr("ublog/dashboard/page.html",
                      {"content": rendered_form,
                       "title": _("New Post")},
                      context_instance=RequestContext(request))

        # If new_post form is not valid
        return on_invalid_form(new_post_form)

    else:
        return HttpResponseForbidden()



@staff_member_required
def save_post(request):
    """
    Last step of saving a post object.
    """
    if "new_post_data" not in request.session:
        raise Http404()

    if not "new_post_type_form" in request.session:
        return HttpResponseForbidden()

    if not "new_post_data" in request.session:
        return HttpResponseForbidden()

    domain = request.get_host()
    try:
        site = Site.objects.get(domain=domain)
    except Site.DoesNotExist:
        raise Http404()

    prev_data = request.session["new_post_data"]
    TypeForm = request.session["new_post_type_form"]
    form = TypeForm(request.POST)

    if form.is_valid():


        from ultra_blog.models import Post, Category

        a = form.save()
        post = Post()
        post.title = prev_data["title"]
        post.slug = prev_data["slug"]
        post.publish = prev_data["publish"]
        post.tags = prev_data["tags"]
        post.author = request.user
        post.site = site
        post.post_type_name = PT.get_form(prev_data["post_type"])
        post.content_object = a
        post.save()

        post.categories = prev_data["categories"]
        post.save()

        return HttpResponseRedirect(reverse("ultra_blog.dashboard.views.index", args=[]))

    rendered_form = rs("ublog/dashboard/forms.html",
                       {"action":
                        reverse("ultra_blog.dashboard.views.new_post",
                                args=[]),
                        "form": form},
                       context_instance=RequestContext(request))

    return rr("ublog/dashboard/page.html",
              {"content": rendered_form,
               "title": _("New Post")},
              context_instance=RequestContext(request))


@staff_member_required
def posts(request):
    """
    Posts index.
    """
    return rr("ublog/dashboard/grid.html",
              {"url": reverse("ultra_blog.dashboard.views.posts_json",
                              args=[])},
              context_instance=RequestContext(request))


@staff_member_required
def posts_json(request):
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
