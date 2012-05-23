# ---------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011-2012 Some Hackers In Town
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
# ---------------------------------------------------------------------------

from django import forms
from django.utils.translation import ugettext as _

from ultra_blog.models import Status, Category
from ultra_blog.base import post_types as PT


class QMicroPostForm(forms.Form):
    """
    Add new micro post.
    """
    status = forms.ChoiceField(label=_("status"))
    message = forms.CharField(label=_("Message"))

    def __init__(self):
        super(QMicroPostForm, self).__init__()
        self.fields['status'].choices = [(i.id, i.name) for i in Status.objects.all()]


class QNewPostForm(forms.Form):
    """
    Quick post form. (post form part 1).
    """
    title = forms.CharField(label=_("title"))
    categories = forms.MultipleChoiceField(label=_("Categories"))
    tags = forms.CharField(label=_("tags"), required=False,
                           help_text=_("use ',' or space as separator."))
    post_type = forms.ChoiceField(label=_("Post type"))

    def __init__(self, request):
        super(QNewPostForm, self).__init__()
        cats = Category.objects.filter(site__domain=request.META["HTTP_HOST"])
        self.fields["categories"].choices = [(i.id, i.title) for i in cats]
        self.fields["post_type"].choices = PT.get_types_dict()
