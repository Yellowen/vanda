# -----------------------------------------------------------------------------
#    Vanda forum - forum application for vanda platform
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

from django.contrib import admin

from models import Category, Setting, Post


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface class for category model
    """
    list_display = ("title", "slug", "parent", "user", "date")
    search_fields = ("title", )
    list_filter = ("user", )
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class PostAdmin(admin.ModelAdmin):
    """
    Admin interface class for post model
    """
    list_display = ("title", "slug", "author", "date")
    search_fields = ("title", "author")
    list_filter = ("author", )
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class SettingAdmin(admin.ModelAdmin):
    """
    Admin interface class for setting model
    """
    list_display = ("title", "active", "anonymous_post",
                    "pre_moderation", "ppp")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Setting, SettingAdmin)
