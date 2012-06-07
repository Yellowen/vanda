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
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from tagging.fields import TagField
from tagging.utils import get_tag_list


class UltraModel(models.Model):

    def get_dict(self, fields):
        values_dict = {}
        for field in fields:
            field_name = field.split(".")[0]
            if hasattr(self, field_name):
                values_dict[field_name] = self
                for prop in field.split("."):
                    values_dict[field_name] = getattr(values_dict[field_name],
                                                      prop)
                values_dict[field_name] = unicode(values_dict[field_name])
            else:
                raise ValueError("'%s' class does not have '%s' attr." % (
                    self.__class__.__name__,
                    field))

        return values_dict

    class Meta:
        abstract = True
        app_label = "ultra_blog"


class Category(UltraModel):
    """
    Each post will be tagged for just one category.
    """

    title = models.CharField(max_length=250,
                             verbose_name=_("Title"))
    slug = models.SlugField(max_length=100,
            verbose_name=_("Slug"),
            help_text=_("This Field will fill automaticaly by title"))

    parent = models.ForeignKey('self', verbose_name=_("Parent"),
                               blank=True, null=True)

    site = models.ForeignKey(Site, verbose_name=_("Site"),
                             null=True, blank=True)

    def get_childs(self):
        return Category.objects.filter(parent=self)

    def count_posts(self):
        """
        Return the number of posts in this category.
        """
        return self.ultra_blog_posts.all().count()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ultra_blog.views.view_category', args=[self.slug])

    class Meta:
        unique_together = (('site', 'slug'))
        app_label = "ultra_blog"
        verbose_name_plural = _("Categories")
        verbose_name = _('Category')
        ordering = ["title"]


class Post (UltraModel):
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
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"),
                                        related_name="%(app_label)s_posts")
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
                               related_name="ultra_blog_post",
                               editable=False,
                               verbose_name=_("Author"))
    datetime = models.DateTimeField(auto_now_add=True, editable=False,
                                     verbose_name=_('Date and Time'))

    update_datetime = models.DateTimeField(null=True, blank=True,
                                           editable=False,
                                           verbose_name=_('Last Update'))

    site = models.ForeignKey(Site, verbose_name=_("Site"),
                             null=True, blank=True)

    objects = models.Manager()
    sites = CurrentSiteManager()

    def is_updated(self):
        """
        Return True if post has been updated.
        """
        if self.update_datetime:
            if self.datetime != self.update_datetime:
                return True
        return False

    def save(self, *args, **kwargs):

        # First save is for initilizing datetime field
        super(Post, self).save(*args, **kwargs)

        # Checking the time difference between save time and the time spend
        # to calculate time delta
        import datetime

        # Its impossible that calculating delta time took more that 30 seconds
        delta = datetime.datetime.now() - datetime.timedelta(seconds=30)

        # If datetime was less that time delta that means that user updated the
        # post otherwise its just been created
        if self.datetime < delta:
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

    def get_categories(self):
        """
        Return the categories list.
        """
        return self.categories.all()

    def get_tags(self):
        return get_tag_list(self.tags)

    def comments_count(self):
        """
        Return the number of comments related to current post.
        """
        return "<a href='#'>%s</a>" % Comment.objects.filter(
            content_type=self).count()

    comments_count.allow_tags = True

    def related_posts(self):
        # TODO: return the posts in same category with same tags
        return Post.objects.filter(categories__in=self.categories.all())[5]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ultra_blog.views.view_post", args=[self.slug])

    class Meta:
        app_label = "ultra_blog"
        ordering = ["-datetime"]
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')
