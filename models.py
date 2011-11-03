# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Some Hackers In Town
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
from django.contrib.admin.models import User
from django.utils.translation import ugettext as _


class Category(models.Model):
    """
    Each post will be tagged for just one category.
    """

    title = models.CharField(max_length=250,
                             unique=True, verbose_name=_("Title"))
    slug = models.SlugField(max_length=100,
                            verbose_name=_("Slug"),
                            help_text=_("This Field will fill\
                            automaticaly by title"))

    parent = models.ForeignKey('self', verbose_name=_("Parent"),
                               blank=True, null=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('ultra_blog.views.category_view', self.slug)

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _('Category')
        ordering = ["title"]


class Post (models.Model):
    """
    Post model.
    author and datetime will be filled automaticly.
    """
    title = models.CharField(max_length=250, verbose_name=_("Title"))
    slug = models.SlugField(max_length=100, verbose_name=_("Slug"),\
                            unique=True,\
                            help_text=_("This field will fill automaticly \
                            by title field."))
    content = models.TextField(verbose_name=_("Content"))
    content_html = models.TextField(_("HTMLized content"))
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"))
    author = models.ForeignKey(User, verbose_name=_("Author"))
    datetime = models.DateTimeField(auto_now_add=True, editable=False,\
                                     verbose_name=_('Date and Time'))

    def get_content(self):
        """
        Return suitable content by looking up settings.
        """
        return self.content

    def comments(self):
        """
        Return the comments related to current post.
        """
        return Comment.objects.filter(post=self)

    def related_posts(self):
        # TODO: return the posts in same category with same tags
        return Post.objects.filter(categories__in=self.categories.all())[5]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("ultra_blog.views.post_view", self.slug)

    class Meta:
        ordering = ["-datetime"]
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')


class Setting (models.Model):
    """
    Configuration model.
    """
    _DEFAULT = {
        'post_per_page': 10,
        'comment_per_page': 10,
        }
    active = models.BooleanField(_("Active"),
                                 default=False)

    post_per_page = models.IntegerField(default=10,
                            verbose_name=_("How many post per page?"))

    comment_per_page = models.IntegerField(default=10,
                            verbose_name=_("How many comment per page?"))

    @staticmethod
    def get_setting(setting_name, default=None):
        """
        Return the field data of given setting_name if exists or
        return default value for it.
        """
        if setting_name in _DEFAULT:
            try:
                return getattr(Setting.objects.get(active=True), setting_name)
            except Setting.DoesNotExist:
                return _DEFAULT[setting_name]
        else:
            return default

    def save(self, *argc, **kwargs):
        """
        Only one active setting allowed.
        """
        if self.active:
            try:
                pre = Setting.objects.get(active=True)
            except Setting.DoesNotExist:
                pass
            pre.save()
        super(Setting, self).save(*argc, **kwargs)

    class Meta:
        verbose_name_plural = _("Settings")
        verbose_name = _('Setting')
