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

    def __init__(self, *args, **kwargs):
        super(QMicroPostForm, self).__init__(*args, **kwargs)
        q = [(i.id, i.name) for i in Status.objects.all()]
        self.fields['status'].choices = q


class QNewPostForm(forms.Form):
    """
    Quick post form. (post form part 1).
    """
    title = forms.CharField(label=_("title"))
    slug = forms.CharField(label=_("Slug"))
    categories = forms.MultipleChoiceField(label=_("Categories"))
    tags = forms.CharField(label=_("tags"), required=False,
                           help_text=_("use ',' or space as separator."))
    post_type = forms.ChoiceField(label=_("Post type"))
    publish = forms.BooleanField(label=_("Publish"), required=False)

    def __init__(self, request, *args, **kwargs):
        obj = None
        self.request = request
        if "instance" in kwargs:
            obj = kwargs["instance"]
            self.instance = obj
            del kwargs["instance"]

        super(QNewPostForm, self).__init__(*args, **kwargs)
        cats = Category.objects.filter(site__domain=request.get_host())
        self.fields["categories"].choices = [(i.id, i.title) for i in cats]
        self.fields["post_type"].choices = PT.get_types_dict()

        if obj:
            del self.fields["post_type"]
            self.fields["title"].initial = obj.title
            self.fields["slug"].initial = obj.slug
            q = obj.categories.all()
            self.fields["categories"].initial = [i.id for i in q]
            self.fields["tags"].initial = obj.tags
            self.fields["publish"].initial = obj.publish

    def save(self):
        data = self.request.POST
        obj = self.instance
        obj.title = data["title"]
        obj.slug = data["slug"]
        q = [int(i) for i in data.getlist("categories")]
        obj.categories = q
        obj.tags = data["tags"]
        obj.publish = data["publish"]
        obj.save()
        return obj
