# ---------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------


from django.conf.urls.defaults import patterns, url

from feeds import LatestPosts, CategoryFeed


urlpatterns = patterns('',
        url(r'^posts/([^/]+)/$', "ultra_blog.views.view_post",
            name="view-post"),
        (r'^tags/([^/]+)/$', "ultra_blog.views.view_tag"),
        (r'^categories/([^/]+)/$', "ultra_blog.views.view_category"),
        (r'^types/(\w+)/$', "ultra_blog.views.view_type"),
        (r'^filter/$', "ultra_blog.views.filter"),
        (r'^feed/category/(?P<slug>\w+)/$', CategoryFeed()),
        (r'^feed/$', LatestPosts()),
        (r'^api/micro/$', 'ultra_blog.views.micro_api'),
        url(r'^new/comment/$', 'ultra_blog.comments.post_comment',
            name="new-ucomment"),
        (r'^$', "ultra_blog.views.blog_index"),
)
