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
from django.template import Context
from apps.jqmenu.models import Menu
from apps.jqmenu.models import MenuItem
from django.template.loader import get_template

register = template.Library()


# {% jqmenu "menu slug" %} defination. --------------------------------------------------------

def do_jqmenu(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, menu_title = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (menu_title[0] == menu_title[-1] and menu_title[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return menu_node(menu_title[1:-1])


class menu_node(template.Node):
    def __init__(self, title):
        self.slug = title

    def render (self , context):
        menu = Menu.objects.get(slug = self.slug)
        menumainitem = MenuItem.objects.filter(menu = menu , hasparent = True ).order_by("order")
        menuitem = MenuItem.objects.filter(menu = menu ,hasparent = False ).order_by("order")
        ent = { "menu" : menu , "menumainitem" : menumainitem , "menuitem" : menuitem }
        t = get_template("jqmenu.html")      
        return t.render(Context(ent, autoescape=context.autoescape))

register.tag ('jqmenu' , do_jqmenu)
