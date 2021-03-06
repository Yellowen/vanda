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


class PostRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_("First Name"))
    last_name = forms.CharField(max_length=30, label=_("Last Name"))
    password1 = forms.CharField(max_length=250, label=_("Password"),
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=250, label=_("Enter again"),
                                widget=forms.PasswordInput())

    def save(self, user):
        """
        Save the cleaned data to User model.
        """
        if not user:
            raise self.NoUser()

        data = self.cleaned_data
        if not data["password1"] == data["password2"]:
            raise self.PasswordError(_("You entered to different password"))

        password = data["password1"]
        if len(password) < 6:
            raise self.PasswordError(
                _("Password length should be more that six charachter"))

        user.set_password(password)
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()

        return True

    class NoUser(Exception):
        pass

    class PasswordError(Exception):
        pass
