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


from django.conf.urls.defaults import patterns, include, url

from tables import (posts, categories, comments)


urlpatterns = patterns('',
    (r'^new/micro/$', 'ultra_blog.dashboard.views.micro_post'),

    # Posts
    url(r'^posts/delete/$', 'ultra_blog.dashboard.views.delete_post',
        name="delete-post"),
    url(r'^posts/edit/(\d+)/$', 'ultra_blog.dashboard.views.edit_post',
        name="edit-post"),
    url(r'^posts/edit/(\w+)/(\d+)/$',
        'ultra_blog.dashboard.views.edit_post_type',
        name="edit-post-type"),

    url(r'^posts/', include(posts.urls)),
    (r'^save/post/$', 'ultra_blog.dashboard.views.save_post'),

    (r'^new/post/$', 'ultra_blog.dashboard.views.new_post'),

    # Categories
    url(r'^categories/delete/$', 'ultra_blog.dashboard.views.delete_category',
        name="delete-category"),
    url(r'^categories/add/$', 'ultra_blog.dashboard.views.add_category',
        name="add-category"),
    url(r'^categories/', include(categories.urls)),
    url(r'^categories/edit/(\d+)/$', 'ultra_blog.dashboard.views.edit_category',
        name="edit-category"),

    # comments
    url(r'^comments/', include(comments.urls)),
    url(r'^comments/delete/$', 'ultra_blog.dashboard.views.delete_comment',
        name="delete-comment"),
    url(r'^comments/change/public/(\d+)/$',
        'ultra_blog.dashboard.views.edit_comment_public',
        name="edit-comment-public"),

    (r'^$', 'ultra_blog.dashboard.views.index'),
)
