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
from django.contrib.comments.models import Comment

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

    def return_child(self):
        cats = Category.objects.filter(parrent=self)
        #for cat in cats:

    class Meta:
        app_label = "ultra_blog"
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

    tags = TagField(_("Tags"),
        help_text=_("Tags should separate with a white space or a comma"))

    publish = models.BooleanField(_("Publish"), default=True,
                        help_text=_("Should post appear in the main page?"))

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

    def delete(self, *args, **kwargs):
        self.comments().delete()
        tmp = self.content_object
        tmp.delete()
        super(Post, self).delete(*args, **kwargs)

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
        return Comment.objects.filter(content_type=self)

    def comments_count(self):
        """
        Return the number of comments related to current post.
        """
        return "<a href='#'>%s</a>" % Comment.objects.filter(content_type=self).count()

    comments_count.allow_tags = True

    def related_posts(self):
        # TODO: return the posts in same category with same tags
        return Post.objects.filter(categories__in=self.categories.all())[5]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("ultra_blog.views.post_view", self.slug)

    class Meta:
        app_label = "ultra_blog"
        ordering = ["-datetime"]
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')
