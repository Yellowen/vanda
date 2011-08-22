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
from django.template import Template, Context
#from dina import conf


class Category(models.Model):
    """
    each post will be tagged for just one category.
    """

    title = models.CharField(max_length=250,\
                             unique=True, verbose_name=_("Title"))
    slug = models.SlugField(max_length=100,\
                            verbose_name=_("Slug"),\
                            help_text=_("This Field will fill\
                            automaticaly by title"))
    
    #Icon = models.ImageField(upload_to="//",verbose_name=_("Description"))
#    CATS = (
#        ('text', _('Text')),
#        ('link', _('Link')),
#        ('music', _('Music')),
#        ('book', _('Book')),
#        ('film', _('Film')),
#        ('person', _('Person or band')),
#    )
    category_type = models.CharField(max_length=250, \
                                      verbose_name=("Type"),)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _('Category')
        ordering = ["title"]


class Post (models.Model):
    """
    Post model.
    Notes:
          Use get_content() instead of content
          author and datetime will be filled automaticly.
    """
    title = models.CharField(max_length=250, verbose_name=_("Title"))
    slug = models.SlugField(max_length=100, verbose_name=_("Slug"),\
                            unique=True,\
                            help_text=_("This field will fill automaticly \
                            by title field."))
    body = models.TextField(verbose_name=_("Content"))
    categoriey = models.ForeignKey(Category, verbose_name=_("Categories"))
    author = models.ForeignKey(User, verbose_name=_("Author"))
    datetime = models.DateTimeField(auto_now_add=True, editable=False,\
                                     verbose_name=_('Date and Time'))

    def get_content(self):
        """
        Return suitable content by looking up settings.
        """
        setting = Setting.configs()
        maxbl = 400
        if setting.max_body_length:
            maxbl = setting.max_body_length
        # TODO: add ... to end of content
        return self.content()
        #return Template("%s<p> ...</p>" % self.body[:maxbl]
        #                          ).render(Context())

    def content(self):
        """
        return HTMLize body content.
        """
        return Template(self.body).render(Context())

    def comments(self):
        """
        Return the comments related to current post.
        """
        return Comment.objects.filter(post=self).order_by('-datetime')

    def related_posts(self):
        return Post.objects.filter(categories__in=self.categories.all())[5]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/post/%s" % self.slug

    class Meta:
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')


class Comment (models.Model):
    """
    Comment model.
    Notes:
           Author of a comment may be empty if 'allow_anonymous' config set
           to True. In this case nick will hold the nickname that user provided

           But if author filled with current user->username then nick fill with
           the same value.
    """

    post = models.ForeignKey(Post, verbose_name=_("Post"))
    author = models.ForeignKey(User, verbose_name=_("Author"), blank=True,\
                                null=True)
    nick = models.CharField(max_length=40,
                            verbose_name=_("Nickname"), blank=True,\
                            null=True)
    email = models.EmailField(blank=True, null=True,
                              verbose_name=_("Email (Optional)"))
    content = models.TextField(verbose_name=_("Your Comment"))
    datetime = models.DateTimeField(auto_now_add=True, editable=False,\
                                     verbose_name=_('Date and Time'))

    def __unicode__(self):
        return "Comment on %s - %s" % (
            self.post.title, "%s..." % self.content[:30])

    def get_absolute_url(self):
        return "/blog/comments/%s" % self.id

    class Meta:
        verbose_name_plural = _("Comments")
        verbose_name = _('Comment')


class Setting (conf.Config):
    """
    Configuration model.
    """
    allow_anonymous_comment=conf.BooleanField(default=True,\
                        verbose_name=_("Allow anonymous comments?"),\
                        help_text=_("Allow to un-registered user to\
                        comment your posts."))
    post_per_page = conf.IntegerField(default=10,\
                            verbose_name=_("How many post per page?"))
    comment_per_page = conf.IntegerField(default=10,\
                            verbose_name=_("How many comment per page?"))
    max_body_length = conf.IntegerField(default=400,\
                            verbose_name=_("Maximume content"),\
                            help_text=_("Maximume character in content"))
    categories_count = conf.IntegerField(default=20,\
                            verbose_name=_("Categories count"),\
                            help_text=_("The number of categories shown in\
                            side bar."))

    class Meta:
        verbose_name_plural = _("Blog Settings")
        verbose_name = _('Setting')

    class ConfigAdmin:
        fieldsets = (
        (None, {
            'fields': (('allow_anonymous_comment',\
                        'max_body_length'),\
                       ('post_per_page',\
                        'comment_per_page',\
                        'categories_count'))
        }),
    )
