from django import template

from ultra_blog.models.base import Category


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
        cats = Category.objects.filter(parent=cat)
        result = ""
        for cat in cats:
            result += """
            <ul>
            <li><input type="checkbox" name="catsgroup" value="%s" />&nbsp;%s</li>    
            """ % (cat.title,cat.title)
            result += self.get_categories(cat)
            result += """
            </ul>
            """
        return template.Template(result).render(template.Context())

register.tag('categorieslist', categories_list)
