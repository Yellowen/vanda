# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Behnam AhmadKhanBeigi ( b3hnam@gnu.org )
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
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from models import Post, Setting


def blog_index(request):
    """
    Render the lastest blog entries.
    """
    ppp = Setting.get_setting("post_per_page")
    post_list = Post.objects.all()

    paginator = Paginator(post_list, ppp)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        postss = paginator.page(paginator.num_pages)

    return rr('ultra_blog/index.html',
              {"posts": posts},
              context_instance=RequestContext(request))


def view_post(request, slug):
    """
    View a single post.
    """
    post = get_object_or_404(Post, slug=slug)

    return rr("ultra_blog/view_post.html",
              {"post": post},
              context_instance=RequestContext(request))


def view_by_type(request, type_name):
    """
    View categories of a type
    """
    posts = Post.objects.filter(post_type_name=type_name)
        
