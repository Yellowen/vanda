# ---------------------------------------------------------------------------------
#    Dina Project
#    Copyright (C) 2010  Dina Project Community
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
# ---------------------------------------------------------------------------------

from django import template
from django.template.loader import get_template
from django.template import Context


from apps.simpleblog.models import Category, Setting

register = template.Library()


def do_categories(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError,\
              "%r tag requires a single argument" % token.contents.split()[0]
    if len(tag_name) > 1:
        raise template.TemplateSyntaxError,\
              "%r tag did not tak an argument" % token.contents.split()[0]
    return Categories()


class Categories(template.Node):
    """
    This class will render latest 'counts' categories.
    """

    def render(self, context):
        setting = Setting.configs()
        categories = Category.objects.all()[:setting.categories_count]
        template = get_template('categories.html')
        return template.render(Context({"categories": categories}))


register.tag('categories', do_categories)
