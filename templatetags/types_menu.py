from django import template
from ultra_blog.base import post_types

register = template.Library()


def types_menu(parser, token):
    return typesNode()


class typesNode(template.Node):
    def render(self, context):
        """
        Get types for menu
        """
        types = post_types.get_all_admin_forms()
        result = ""
        for type_ in types:
            result += """
                <li>
                <a href="/blog/filter/%s">%s</a>
                </li>
            """ % (type_[0], type_[0])
        return template.Template(result).render(template.Context())


register.tag('typesmenu', types_menu)
