# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
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
# ---------------------------------------------------------------------------------

from django.db import models
from django.contrib.admin.models import User
from django.utils.translation import ugettext as _

from dina import conf

def Category (models.Model):
    """
    each post will be tagged for several category.
    """
    title = models.CharField (max_length=250, verbose_name=_("Title"))
    slug = models.SlugField (max_length=100, verbose_name=_("Slug"),\
                             help_text = _("This Field will fill automaticaly by title"))
    description = models.TextField(verbose_name=_("Description"))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _('Category')


def Post (models.Model):
    title = models.CharField (max_length=250, verbose_name=_("Title"))
    slug = models.SlugField (max_length=100, verbose_name=_("Slug"),\
                             help_text = _("This field will fill automaticly by title field."))
    content = models.TextField (verbose_name=_("Title"))
    categories = models.ManyToManyField (Category, verbose_name=_("Categories"))
    author = models.ForeignKey (User, verbose_name=_("Author"))
    datetime = models.DateTimeField (auto_now_add=True, editable=False,\
                                     verbose_name=_('Date and Time'))

    def __unicode__ (self):
        return self.title
    
    def get_absolute_url (self):
        return "/blog/post/%s" % self.slug
    
    class Meta:
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')



def Comment (models.Model):
    post = models.ForeignKey (Post, verbose_name=_("Post"))
    author = models.ForeignKey (User, verbose_name=_("Author"), blank=True,\
                                null=True)
    nick = models.CharField (max_length=40, verbose_name=_("Nickname"), blank=True,\
                                null=True)
    content = models.TextField (verbose_name=_("Title"))
    datetime = models.DateTimeField (auto_now_add=True, editable=False,\
                                     verbose_name=_('Date and Time'))

    def __unicode__ (self):
        return "Comment on %s - %s" % (self.post.title, "%s..." % self.content[:30])
    
    def get_absolute_url (self):
        return "/blog/comments/%s" % self.id
    
    class Meta:
        verbose_name_plural = _("Comments")
        verbose_name = _('Comment')


def setting (conf.Config):
    allow_anonymous_comment = conf.BooleanField (default=False,\
                                    verbose_name=_("Allow anonymous comments?"),\
                                    help_text=_("Allow to un-registered user to comment your posts."))
    post_per_page = conf.IntegerField (default=10, verbose_name=_("How many post per page?"))

    class Meta:
        verbose_name_plural = _("Blog Settings")
        verbose_name = _('Setting')

    
