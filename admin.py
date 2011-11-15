
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
# ----------------------------------------------------------------------------

from django import forms
from django.contrib import admin
from django.conf.urls.defaults import url, patterns
from django.utils.html import escape
from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.utils.encoding import force_unicode
from django.contrib.admin.options import csrf_protect_m
from django.db import models, transaction
from django.utils.functional import curry
from django.forms.models import modelform_factory
from django.contrib.admin import widgets, helpers
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.admin.util import (unquote, flatten_fieldsets,
                                       get_deleted_objects, model_format_dict)

from forms import NewPostForm, EditPostForm
from models import Category, Post, Setting, TextPost
from base import post_types


class CategoryAdmin(admin.ModelAdmin):
    """
    Category model admin.
    """
    list_display = ("title", "slug", "parent")
    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    """
    Post admin interface.
    """
    list_display = ("title", "author", "comments_count", "tags", "datetime",
                    "update_datetime", "publish", "post_type")

    list_filter = ("categories", )
    filter_horizontal   = ("categories", )
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}

    def get_urls(self):

        urlpatterns = patterns('',
            (r'^add/(\w+)/$', self.add_post),
            (r'^add/\w+/(\d+)/$', self.change_view),
        )
        urlpatterns += super(PostAdmin, self).get_urls()
        return urlpatterns

    def get_form(self, request, obj=None, **kwargs):
        """
        Returns a Form class for use in the admin add view. This is used by
        add_view and change_view.
        """

        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        exclude = self.exclude

        defaults = {
            "form": NewPostForm,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": curry(self.formfield_for_dbfield,
                                        request=request),
        }
        if obj:
            #setattr(EditPostForm, "posttype", obj.post_type_name)
            defaults["form"] = EditPostForm

        defaults.update(kwargs)
        return modelform_factory(self.model, **defaults)

    @csrf_protect_m
    @transaction.commit_on_success
    def add_post(self, request, post_type):
        """
        Render the form for post_type
        """
        if not "postdata" in request.session:
            raise Http404()
        if not "post_type" in request.session["postdata"]:
            raise Http404()

        self.fieldsets = None
        # Get the type class and its needed properties
        type_name = request.session["postdata"]["post_type"]
        type_class = post_types.get_type(type_name)
        ModelForm = type_class.admin_form
        model = ModelForm.Meta.model
        if type_class.admin_class is not None:
            admin_class = type_class.admin_class(model, self.admin_site)
        else:
            tmp = type("AdminClass", (admin.ModelAdmin, ),
                               {})
            admin_class = tmp(model, self.admin_site)
            setattr(admin_class, "form", ModelForm)
        model = ModelForm.Meta.model
        opts = model._meta
        formsets = []
        form_url = ''
        if request.method == "POST":
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                new_object = form.save()
                new_post = Post()
                new_post.title = request.session["postdata"]["title"]
                new_post.slug = request.session["postdata"]["slug"]
                new_post.author = request.user
                new_post.page_title = request.session["postdata"]["page_title"]
                new_post.description = request.session["postdata"]["description"]
                new_post.tags = request.session["postdata"]["tags"]
                new_post.publish = request.session["postdata"]["publish"]
                new_post.content_object = new_object
                new_post.save()

                new_post.post_type_name = post_type
                new_post.categories = request.session["postdata"]["categories"]
                new_post.save()

                admin_class.save_model(request,
                                       new_object,
                                       form,
                                       change=False)

                del request.session["postdata"]

                self.log_addition(request, new_object)
                #return self.response_add(request, new_object)
                #return self.changelist_view(request)

                return HttpResponseRedirect(
                    reverse("admin:%s_%s_changelist" % (
                        self.model._meta.app_label,
                        self.model.__name__.lower()), args=()))
        else:
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(initial=initial)
            prefixes = {}
            for FormSet, inline in zip(admin_class.get_formsets(request),
                                       admin_class.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=model(), prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(admin_class.get_fieldsets(request)),
            admin_class.prepopulated_fields, admin_class.get_readonly_fields(request),
            model_admin=admin_class)
        media = admin_class.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(admin_class.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            readonly = list(inline.get_readonly_fields(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=admin_class)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': admin_class.admin_site.root_path,
            'app_label': opts.app_label,
        }
        return admin_class.render_change_form(request,
                                       context,
                                       form_url=form_url,
                                       add=True)

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        self.fields = None
        self.fieldsets = None
        ModelForm = self.get_form(request)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)

            if form.is_valid():
                request.session["postdata"] = form.cleaned_data
                return HttpResponseRedirect("%s/" % form.cleaned_data["post_type"])
        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            if "postdata" in request.session: del request.session["postdata"]

            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            self.fields = None
            form = ModelForm(initial=initial)
            self.fields = form.fields.keys()
            self.fieldsets = (
                (None, {"fields": (("title", "slug", "post_type"),
                                   ("categories", "tags"),
                                   "publish")}),
                (_("SEO"), {"fields": ("page_title", "description"),
                            "description": _("Search Engine Optimization options.")}),
                )

            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request),
                                       self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=self.model(), prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.prepopulated_fields, self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            readonly = list(inline.get_readonly_fields(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context,
                                       form_url=form_url, add=True)

    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(
                _('%(name)s object with primary key %(key)r does not exist.') \
                % {'name': force_unicode(opts.verbose_name),
                   'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url='../add/')

        self.fields = None
        self.fieldsets = None
        ModelForm = self.get_form(request, obj)
        formsets = []
        if request.method == 'POST':

            form = ModelForm(obj.post_type_name, request.POST,
                             request.FILES, instance=obj)
            self.fields = form.fields.keys()

            if form.is_valid():
                form_validated = True
                # new_object = self.save_form(request, form, change=True)
                new_object = form.save(request)
                # TODO: Review this algorithm
                return self.response_change(request, new_object)
            else:
                form_validated = False
                new_object = obj
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, new_object),
                                       self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(request.POST, request.FILES,
                                  instance=new_object, prefix=prefix,
                                  queryset=inline.queryset(request))

                formsets.append(formset)

            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=True)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=True)

                change_message = self.construct_change_message(request,
                                                               form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)

        else:
            self.fields = None
            form = ModelForm(obj.post_type_name, instance=obj)
            self.fields = form.fields.keys()
            
            tmp = [
                (None, {"fields": (("title", "slug", "post_type"),
                                   ("categories", "tags"),
                                   "publish")}),
                (_("SEO"), {"fields": ("page_title", "description")}),
            ]
            external_fieldset = form.get_fieldset()

            if external_fieldset:
                tmp.append(external_fieldset)

            self.fieldsets = tuple(tmp)

            prefixes = {}
            for FormSet, inline in zip(
                self.get_formsets(request, obj),
                self.inline_instances):

                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
            self.prepopulated_fields, self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': "_popup" in request.REQUEST,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)


class SettingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Setting, SettingAdmin)
#admin.site.register(TextPost)
