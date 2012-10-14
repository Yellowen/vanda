from django import forms
from django.utils.translation import ugettext as _


class ContactUs(forms.Form):
    name = forms.CharField(max_length=30, label=_('Name'))
    family = forms.CharField(max_length=30, label=_('Family'))
    email = forms.EmailField(label=_('E-mail'))
    message = forms.CharField(widget=forms.Textarea, label=_('Message'))
