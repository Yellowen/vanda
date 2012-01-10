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

import datetime

from haystack import site
from haystack import indexes

from models import Post, TextPost


class PostIndex(indexes.SearchIndex):
    post_title = indexes.CharField(document=True)
    description = indexes.CharField()
    post_type_name = indexes.CharField()

    def get_queryset(self):
        """
        This is used when the entire index for model is updated, and should only include
        public entries
        """
        return Post.objects.filter(datetime__lte=datetime.datetime.now())

site.register(Post, PostIndex)
