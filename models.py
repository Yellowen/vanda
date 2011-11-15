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
from django.contrib.contenttypes import generic

from tagging.fields import TagField


class Category(models.Model):
    """
    Each post will be tagged for just one category.
    """

    title = models.CharField(max_length=250,
                             unique=True, verbose_name=_("Title"))
    slug = models.SlugField(max_length=100,
            verbose_name=_("Slug"),
            help_text=_("This Field will fill automaticaly by title"))

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
    title = models.CharField(max_length=64, verbose_name=_("Title"))
    slug = models.SlugField(max_length=64, verbose_name=_("Slug"),
            unique=True,
            help_text=_("This field will fill automaticly by title field."))

    content_type = models.ForeignKey('contenttypes.ContentType',
                                     editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"))
    post_type_name = models.CharField(_("Post type name"),
                                      max_length=30,
                                      blank=True)

    tags = TagField(_("Tags"))

    draft = models.BooleanField(_("Draft"), default=True)

    page_title = models.CharField(_("Page title"),
                                  max_length=128,
                                  blank=True,
                                  default="")
    description = models.TextField(_("page description"),
                                   blank=True, null=True)

    author = models.ForeignKey(User,
                               editable=False,
                               verbose_name=_("Author"))
    datetime = models.DateTimeField(auto_now_add=True, editable=False,
                                     verbose_name=_('Date and Time'))

    update_datetime = models.DateTimeField(null=True, blank=True,
                                           editable=False,
                                           verbose_name=_('Last Update'))

    def save(self, *args, **kwargs):
        import datetime
        self.update_datetime = datetime.datetime.now()
        super(Post, self).save(*args, **kwargs)

    def get_content(self):
        """
        Return suitable content by looking up settings.
        """
        return self.content_object.get_htmlized_content()

    def post_type(self):
        """
        Return the post type.
        """
        return str(self.content_object.__class__._meta.verbose_name)

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


class TextPost(models.Model):
    """
    Text post model.
    """
    content = models.TextField(_("Post Content"))
    html_content = models.TextField(_("HTMLized Content"),
                                    blank=True,
                                    null=True)

    def encode_content(self):
        pass

    def get_htmlized_content(self):
        return self.html_content or self.encode_content()

    def __unicode__(self):
        return self.content[:30]

    class Meta:
        verbose_name = _("Text Post")
        verbose_name_plural = _("Text Posts")


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
