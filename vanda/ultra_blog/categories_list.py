# ---------------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------------

from django import template
from models.base import Category
register = template.Library()


def categories_list(parser, token):
    return CategoriesNode()


class CategoriesNode(template.Node):

    def render(self, context):
        return self.get_categories()

    def get_categories(self, cat=None):
        """
        Get categories
        """
        cats = Category.return_child(cat)
        result = ""
        for cat in cats:
            result += """
            <ul>
            <li>%s</li>    
            """ % cat.title
            result += self.get_categories(cat)
            result += """
            </ul>
            """
        return result

register.tag('categories_list', categories_list)
