# -----------------------------------------------------------------------------
#    Vanda news - News application for vanda platform
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

from django import template
from django.template import Template, Context
from django.template.loader import get_template
from django.conf import settings

from news.models import News


register = template.Library()


def render_news_list(parser, token):

    return NewsListNode()


class NewsListNode(template.Node):

    def render(self, context):
        news = News.objects.all().order_by("-date")[:settings.NEWS_LIMIT]
        t = get_template("news_tag.html")
        return t.render(Context({"news_list": news or []}))

register.tag('news', render_news_list)
