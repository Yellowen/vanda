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
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

from models import Post, TextPost, ImagePost
from base import post_types


class TextTypeForm(forms.ModelForm):
    fieldset = (_("Text Post"), {"fields": ("content", )})

    class Meta:
        model = TextPost

    class Media:
        js = ("%sjs/nicEdit.js" % settings.MEDIA_URL,
              "%sjs/js_init.js" % settings.MEDIA_URL,)
        css = {'all': ("%scss/nicss.css" % settings.MEDIA_URL, )}


class ImageTypeForm(forms.ModelForm):
    fieldset = (_("Image Post"), {"fields": (("image", "klass"),
                                             ("width", "height"),
                                             "description")})

    class Meta:
        model = ImagePost


class NewPostForm(forms.ModelForm):
    post_type = forms.ChoiceField(label=_("Post Type"))

    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)

        self.fields["post_type"].choices = post_types.get_all_admin_forms()

    class Meta:
        model = Post
        fields = ["title", "slug", "categories", "tags", "page_title",
                  "description", "publish"]


class EditPostForm(forms.ModelForm):

    post_type = forms.CharField(label=_("Post Type"))

    def __init__(self, posttype, *args, **kwargs):

        obj = kwargs["instance"]

        super(EditPostForm, self).__init__(*args, **kwargs)

        self.fields['post_type'].widget.attrs['readonly'] = True
        self.initial["post_type"] = posttype

        FormClass = post_types.get_form(posttype)

        if FormClass:
            form = FormClass(*args, instance=obj.content_object)
            self.form = form
            if hasattr(form, "fieldset"):
                self.external_fieldset = form.fieldset
            else:
                self.external_fieldset = None

            self.Media = form.Media


        prefix = "%s_" % FormClass.__name__

        for field in form.fields:
            if field in self.fields:
                # TODO: Control the same field names.
                pass
            else:

                self.fields[field] = form.fields[field]
                self.initial[field] = form.initial[field]

    def save(self, request, *args, **kwargs):

        prefix = "%s_" % self.form.__class__.__name__
        self.form.save()
        return super(EditPostForm, self).save(*args, **kwargs)

    def get_fieldset(self):
        return self.external_fieldset

    def is_valid(self):
        if self.form.is_valid():
            super(EditPostForm, self).is_valid()
            return True

        return False

    class Meta:
        model = Post
        exclude = ["post_type_name", ]
