# -----------------------------------------------------------------------------
#    Vanda - Web development platform
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

from django import forms
from django.utils.translation import ugettext as _


class AjaxWidget(forms.TextInput):
    """
    An abstract ajax widget, using this widget cause that form field
    intract with the server via ajax process.
    """

    def __init__(self, field_name, url, *args, **kwargs):
        self.url = url
        self.fname = field_name
        super(AjaxWidget, self).__init__(*args, **kwargs)

    def js(self):
        return "/auth/static/?validator=%s" % self.url

    ## def _media(self):
    ##     return forms.Media(css={'all': ('forms.css', )},
    ##                        js=(self.js(), ))

    ## media = property(_media)


class PreRegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, label=_("Username"),
                               widget=AjaxWidget("asd", "asdasD"))

    email = forms.EmailField(label=_("Email"), widget=AjaxWidget("aaa", "ad"))
