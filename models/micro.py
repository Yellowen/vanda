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
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.db import models
from django.contrib.admin.models import User
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.managers import CurrentSiteManager


# Status model added just because of lxsameercom
class Status(models.Model):
    """
    Status model.
    """
    name = models.CharField(_("Status"), max_length=32,
                            unique=True)

    #site = models.ForeignKey(Site, verbose_name=_("Site"),
    #                         null=True, blank=True)

    #sites = CurrentSiteManager('site')

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "ultra_blog"
        verbose_name_plural = _("Micro Statuses")
        verbose_name = _('Micro Stauts')


class MicroPost(models.Model):
    """
    Micro post model.
    """

    content = models.TextField(_("What's in your mind?"))

    status = models.ForeignKey(Status, verbose_name=_("Status"),
                               blank=True, null=True)

    author = models.ForeignKey(User,
                               editable=False,
                               verbose_name=_("Author"))

    datetime = models.DateTimeField(auto_now_add=True, editable=False,
                                    verbose_name=_('Date and Time'))

    site = models.ForeignKey(Site, verbose_name=_("Site"),
                             null=True, blank=True)

    sites = CurrentSiteManager('site')

    objects = models.Manager()

    class Meta:
        app_label = "ultra_blog"
        ordering = ["-datetime"]
        verbose_name_plural = _("Micro Posts")
        verbose_name = _('Mirco Post')


@receiver(post_save, sender=MicroPost)
def my_handler(sender, **kwargs):
    try:
        from core.websucks.unix import UnixClient

        if kwargs["created"] == True:
            t = get_template("ublog/tags/micro.html")
            send_dict = {"html": t.render(Context({"posts": [kwargs["instance"]]})),
                         "id": "#micro_%s" % kwargs["instance"].pk}

            UnixClient(settings.UNIX_SOCKET).send(send_dict, event="new_log")

    except ImportError:
        return
