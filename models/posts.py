# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Sameer Rahmani <lxsameer@gnu.org>
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
# -----------------------------------------------------------------------------

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from config import Setting


class TextPost(models.Model):
    """
    Text post model.
    """
    content = models.TextField(_("Post Content"))

    def get_htmlized_content(self):

        import re

        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter


        # Loading current highlighting style
        current_style = Setting.get_setting("highlight_style")

        # Find all the code tags
        code_pattern = re.compile("(\[code ([A-Za-z]+)\ *\](.*)\[/code\])",
                                  re.I | re.M | re.S)
        code_sections = code_pattern.findall(self.content)

        result = '<link href="%scss/%s.css" rel="stylesheet">\n%s' % (
            settings.MEDIA_URL, current_style, self.content)

        # Replace the code tags with their rendered HTML
        for raw_text, language, code in code_sections:

            lexer = get_lexer_by_name(language, stripall=True)
            formatter = HtmlFormatter(linenos=True, cssclass="codehilite",
                                      style=current_style)
            tmpresult = highlight(code, lexer, formatter)
            result = result.replace(str(raw_text), tmpresult)

        return result

    def __unicode__(self):
        return self.content[:30]

    class Meta:
        app_label = "ultra_blog"
        verbose_name = _("Text Post")
        verbose_name_plural = _("Text Posts")


class ImagePost(models.Model):
    """
    Image post type.
    """
    image = models.ImageField(upload_to="uploads/imagepost/",
                              verbose_name=_("Image"),
                              help_text=_("Image for the post."))

    alt = models.CharField(_("Image alt"), max_length=255,
                           blank=True,
                           null=True)

    klass = models.CharField(_("CSS class"),
                max_length=64,
                blank=True,
                null=True,
                help_text=_("If did not specified \"image_post\" will used."))

    width = models.IntegerField(_("Image width"),
                                default=0,
                                blank=True,
                                null=True)

    height = models.IntegerField(_("Image height"),
                                default=0,
                                blank=True,
                                null=True)

    description = models.TextField(_("Image description"),
                                   blank=True,
                                   null=True)

    def get_htmlized_content(self):
        result = """
        <div class='image_posts'>
        <img src='%s' alt='%s' class='%s' id='%s' width='%s' height='%s'><br>
        DESC
        </div>
        """

        if self.description:
            result = result.replace("DESC", self.description)
        else:
            result = result.replace("DESC", "")

        return result % ("%s%s" % (settings.MEDIA_URL, self.image),
                         self.alt or "",
                         self.klass or "image_post",
                         "image_%s" % self.id,
                         self.width or "",
                         self.height or "")

    def __unicode__(self):
        return "Image - %s" % self.id

    class Meta:
        app_label = "ultra_blog"
        verbose_name = _("Image Post")
        verbose_name_plural = _("Image Posts")
