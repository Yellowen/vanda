from django import template
from dina.fem.menu.models import *


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
    def render(self, context):
        
        return datetime.datetime.now().strftime(self.format_string)

