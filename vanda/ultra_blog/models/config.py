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
from django.utils.translation import ugettext as _


class Setting (models.Model):
    """
    Configuration model.
    """
    STYLES = [
        ("", "---"),
        ('monokai', 'Monokai'),
        ('manni', 'Manni'),
        ('perldoc', 'Perldoc'),
        ('borland', 'Borland'),
        ('colorful', 'Colorful'),
        ('default', 'Default'),
        ('murphy', 'Murphy'),
        ('vs', 'Vs'),
        ('trac', 'Trac'),
        ('tango', 'Tango'),
        ('fruity', 'Fruity'),
        ('autumn', 'Autumn'),
        ('bw', 'Bw'),
        ('emacs', 'Emacs'),
        ('vim', 'Vim'),
        ('pastie', 'Pastie'),
        ('friendly', 'Friendly'),
        ('native', 'Native'),
        ]

    ANTISPAM = [
        ["0", "TypePad"],
        ["1", "Akismet"],
        ]

    _DEFAULT = {
        'post_per_page': 10,
        'comment_per_page': 10,
        "highlight_style": "emacs",
        "antispam": "0",
        "spam_apikey": None,
        }
    active = models.BooleanField(_("Active"),
                                 default=False)

    post_per_page = models.IntegerField(default=10,
                            verbose_name=_("How many post per page?"))

    comment_per_page = models.IntegerField(default=10,
                            verbose_name=_("How many comment per page?"))

    highlight_style = models.CharField(_("Highlight style"),
                                       max_length=16,
                                       choices=STYLES,
                                       blank=True)

    antispam = models.CharField(_("Anti-Spam"),
                                max_length=1,
                                choices=ANTISPAM,
                                null=True,
                                blank=True)

    spam_apikey = models.CharField(_("Anti-Spam API key"),
                                   max_length=100,
                                   help_text=_("Akismet or Typepad API key"),
                                   null=True,
                                   blank=True)

    @classmethod
    def get_setting(cls, setting_name, default=None):
        """
        Return the field data of given setting_name if exists or
        return default value for it.
        """
        if setting_name in cls._DEFAULT:
            try:
                return getattr(Setting.objects.get(active=True), setting_name)
            except Setting.DoesNotExist:
                return cls._DEFAULT[setting_name]
        else:
            return default

    def save(self, *argc, **kwargs):
        """
        Only one active setting allowed.
        """
        if self.active:
            try:
                pre = Setting.objects.get(active=True)
                if pre is not self:
                    pre.active = False
                    pre.save()
            except Setting.DoesNotExist:
                pass

        super(Setting, self).save(*argc, **kwargs)

    class Meta:
        app_label = "ultra_blog"
        verbose_name_plural = _("Settings")
        verbose_name = _('Setting')
