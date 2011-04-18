from django import forms
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    """
    Login form
    """
    username = forms.CharField(max_length=30,
                               label=_("Username"))
    password = forms.CharField(max_length=50,
                               label=_("Password"),
                               widget=forms.PasswordInput())
