from django import template
from ultra_blog.base import post_types

register = template.Library()


def types_list(parser, token):
    return typesNode()


class typesNode(template.Node):

    def render(self, context):
        return self.get_types()

    def get_types(self, cat=None):
        """
        Get types
        """
        types = post_types.get_all_admin_forms()
        result = ""
        for type_ in types:
            result += """
            <ul>
            <li>
            <input type="checkbox" name="typesgroup" value="%s" />&nbsp;%s
            </li>    
            """ % (type_[0], type_[0])
            result += """
            </ul>
            """
        return template.Template(result).render(template.Context())

register.tag('typeslist', types_list)
