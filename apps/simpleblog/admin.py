from django.contrib import admin
from models import *

class CategoryAdmin (admin.ModelAdmin):
    list_display = ['title', 'slug', 'description']
    prepopulated_fields = {"slug": ("title",)}
    #list_display_links =['title',]
    #list_editable = ['title',]

    
class PostAdmin (admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'datetime', ]
    list_filter = ['author', 'categories']
    search_fields = ['title', 'content',]
    filter_horizontal = ['categories',]
    list_editable = [ 'slug',]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'),'content', 'categories')
        }),
        
    )



    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save ()

class CommentAdmin (admin.ModelAdmin):
    list_display = ['post', 'nick', 'author', 'datetime',]
    list_filter = ['author',]
    search_fields = ['nick', 'content', 'author', 'post']


class SettingAdmin (admin.ModelAdmin):
    pass

admin.site.register (Comment, CommentAdmin)
admin.site.register (Post, PostAdmin)
admin.site.register (Category, CategoryAdmin)
admin.site.register (Setting, SettingAdmin)
