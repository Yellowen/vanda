# newforms deprecated in django 1.x
from django import forms
from django.utils.translation import gettext as _


class SearchForm(forms.Form):
    text = forms.CharField(label=_("Enter search term"))
    search_content = forms.BooleanField(label=_("Search content"),\
                                        required=False)
