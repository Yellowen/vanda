from django import template
from django.template import Template , Context
from dina.fem.menu.models import *
from django.template.loader import get_template
register = template.Library()

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
        submenu = get_template ("test/menu.html")
        item = get_template ("test/item.html")
        res = Template ('').render (Context ())
        con = {"title" : x.title , "submenu" : ""}
        for i in x.get_children ():
            res = res + self.draw_menu (i , context)
        for i in x.items.all () :
            res = res + item.render ( Context ( {"target" : i.url , "title" : i.title } ) )
        con["submenu"] = res
        out = submenu.render ( Context( con ,  autoescape=context.autoescape ) )
        print out
        return  out


    def render(self, context):
        smenu = menu.objects.get (title = self.title)
        output = self.draw_menu (smenu , context)

        return output



register.tag ('menu' , do_menu)
