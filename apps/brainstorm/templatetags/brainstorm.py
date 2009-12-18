from django import template
from django.template import Template , Context
from models import *
from django.template.loader import get_template
from dina.core.dev import dassert
register = template.Library()


# {% brainstorm "section" %} defination. --------------------------------------------------------

def do_brainstorm (parser, token):
    sections = (
        'view',
        'form',
        )
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, section_title = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (section_title[0] == section_title[-1] and section_title[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    if section_title[1:-1] in sections:
        return brainstorm_node(section_title[1:-1])
    else:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    


class brainstorm_node(template.Node):
    def __init__(self, section):
        self.section = section
        
        
    def draw_section (self , x , context):
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
        dassert (out)
        return  out


    def render(self, context):
        cate = category.objects.filter (publish = True).order_by ('title')
        t = get_template (
        for i in cate:
            
# -------------------------------------------------------------------------------------------------
