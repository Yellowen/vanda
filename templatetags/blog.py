# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011-2012 Sameer Rahmani <lxsameer@gnu.org>
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
from django.core.urlresolvers import reverse
from django.template import RequestContext

from ultra_blog.models import MicroPost


register = template.Library()


def latest_micropost(parser, token):
    try:
        tag_name, number = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])

    return MicroPostsNode(int(number))


class MicroPostsNode(template.Node):
    """
    This node represent the latest mirco posts.
    """

    def __init__(self, number):
        self.number = number

    def render(self, context):
        host = context["request"].get_host()
        microposts = MicroPost.objects.filter(site__domain=host)[:self.number]

        rr = template.loader.render_to_string
        return rr("ublog/tags/micro.html", {"posts": microposts},
                  context_instance=RequestContext(context["request"]))


register.tag('microposts', latest_micropost)
