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
from django.template import Template , Context
from dina.fem.menu.models import *
from django.template.loader import get_template
from dina.core.dev import dassert
register = template.Library()


# {% menu "menu title" %} defination. --------------------------------------------------------

def do_menu(parser, token):
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
        self.title = title
        
        
    def draw_menu (self , x , context):
        submenu = get_template ("menu.html")
        item = get_template ("item.html")
        res = Template ('').render (Context ())
        con = {"title" : x.title , "submenu" : ""}
        for i in x.get_children ():
            res = res + self.draw_menu (i , context)
        for i in x.items.all () :
            res = res + item.render ( Context ( {"target" : i.url , "title" : i.title } ) )
        con["submenu"] = res
        out = submenu.render ( Context( con ,  autoescape=context.autoescape ) )
        dassert (out)
        return  out


    def render(self, context):
        smenu = menu.objects.get (title = self.title)
        output = self.draw_menu (smenu , context)

        return output

# -------------------------------------------------------------------------------------------------

# {% menu_class "mclass" %} -----------------------------------------------------------------------

def do_menu_class (parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, menu_class = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (menu_class[0] == menu_class[-1] and menu_class[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return menu_class_node(menu_class[1:-1])


class menu_class_node(template.Node):
    def __init__(self, mclass):
        self.mclass = mclass


        
    def draw_menu (self , x , context):
        menu_t = get_template ("menu_%s.html" % (self.mclass))    

        
        res = Template ('').render (Context ())
        # normal refer to view of menu , if it exist on context menu will render with submenu otherwise just items will rendered .
        con = {"title" : x.title , "submenu" : "" , "items" : [] , "normal" : ""}
        
        for i in x.items.all () :
            con['items'].append (i)
        if x.view == "normal":
            con['normal'] = x.view
            for i in x.get_children ():
                res = res + self.draw_menu (i , context )

        dassert (res)
        if res:
            con["submenu"] = Context (res)
        out = menu_t.render ( Context( con ,  autoescape=context.autoescape ) )
        
        return  out


    def render(self, context):
        smenu = menu.objects.filter (mclass = self.mclass , publish = True , parent = None)
        output = ""
        for i in smenu:
            output = output + self.draw_menu (i , context)
        
        return output

#---------------------------------------------------------------------------------------------------



register.tag ('menu' , do_menu)
register.tag ('menu_class' , do_menu_class)
