# -----------------------------------------------------------------------------
#    Vanda Core - Vanda core utilities
#    Copyright (C) 2011 Sameer Rahmani <lxsameer@gnu.org>
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

# Gravatar template tag
# {% load gravatar %}
# and to use the url do this:
# <img src="{% gravatar_url 'someone@somewhere.com' %}">
# or
# <img src="{% gravatar_url 'sometemplatevariable' %}">

import urllib
import hashlib

from django import template
from django.conf import settings


register = template.Library()


class GravatarUrlNode(template.Node):
    def __init__(self, email, size=None):
        self.email = template.Variable(email)
        self.size = size

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        size = 40
        if self.size:
            size = self.size

        host = context["request"].META["HTTP_HOST"]
        default = "http://%s%simages/defaultavatar.png" % (host, settings.MEDIA_URL)
        gravatar_url = "http://www.gravatar.com/avatar/%s?" % \
                       hashlib.md5(email.lower()).hexdigest()
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
        return gravatar_url


@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email, size = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two argument" % token.contents.split()[0]
    return GravatarUrlNode(email, int(size))
