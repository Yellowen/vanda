from django import template
from django.core.urlresolvers import reverse

from ultra_blog.models.base import Category


register = template.Library()


def categories(parser, token):
    return CategoriesNode()


def categories_list(parser, token):
    return CategoriesListNode()


class CategoriesListNode(template.Node):

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


class CategoriesNode(template.Node):
    """
    Return a list of categories with number of post in their.
    """

    def render(self, content):
        return template.Template(self.make_list()).render(template.Context())

    def make_list(self, cat=None):
        """
        Make a ul list from category.
        """
        cats = Category.objects.filter(parent=cat)
        result = "<ul class=\"categories\">%s</ul>"

        if cats:
            tmp = ""
            for category in cats:
                childs = category.get_childs()
                if childs:
                    tmp = "%s%s" % (
                        tmp,
                        "<li><a href='%s'>%s (%s)</a></li>\n" % (
                            reverse("ultra_blog.views.view_category",
                                    args=[category.slug]),
                            category.title,
                            category.count_posts()))

                    for child in childs:
                        tmp = "%s\n%s" % (tmp,
                                          self.make_list(child))
                else:
                    tmp = "%s%s" % (
                        tmp,
                        "<li><a href='%s'>%s (%s)</a></li>\n" % (
                            reverse("ultra_blog.views.view_category",
                                    args=[category.slug]),
                            category.title,
                            category.count_posts()))

            return result % tmp

        else:
            return result % (
                "<li><a href='%s'>%s (%s)</a></li>\n" % (
                    reverse("ultra_blog.views.view_category",
                            args=[cat.slug]),
                    cat.title,
                    cat.count_posts()))


register.tag('categorieslist', categories_list)
register.tag('categories', categories)
