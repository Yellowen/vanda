# -----------------------------------------------------------------------------
#    Debbox - Modern administration panel for Debian GNU/Linux
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
#from django.template import Context
#from django.template.loader import get_template
from django.conf import settings

from debbox.dashboard.loder import load_dashboard_instance
register = template.Library()


def render_drawer(parser, token):

    return drawer_node()


class drawer_node(template.Node):

    def render(self, context):
        installed_apps = settings.INSTALLED_APPS

        return "||".join(installed_apps)


register.tag('drawer_items', render_drawer)
