from django.contrib import admin
from models import *


class cat_admin (admin.ModelAdmin):
    list_display = ["title"  , "published"]
    list_filter = ["published" ]
    search_field = [ "title" , ]

class storm_admin (admin.ModelAdmin):
    list_display = ["title"  , "category" , "email" , "published" ,  "description"]
    list_filter = ["category", "published" ]
    search_field = [ "title" , "email" ]

class comment_admin (admin.ModelAdmin):
    list_display = ["email"  , "storm" , "comment"]
    list_filter = ["email" , "storm" ]
    search_field = [ "email" , "comment" ]


admin.site.register (category , cat_admin)
admin.site.register (storm , storm_admin)
admin.site.register (comment , comment_admin)
    
