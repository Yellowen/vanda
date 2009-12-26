from django.contrib import admin
from models import *

class admin_post (admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ["title"  , "datetime" , "author" , "text"]
    #+++ month and year filter should add too by adding some methods to entry model
    #--- datetime filter should remove in future
    list_filter = ["datetime" , "author" ]
    search_field = [ "title" , ]

    def save_model (self, request, obj, form, change):
        obj.author = request.user
        obj.save ()


    
class admin_com (admin.ModelAdmin):
    list_display = ["nick"  , "datetime" , "post"]
    
    list_filter = ["datetime" ,  ]
    search_field = [ "nick" , ]



admin.site.register (post , admin_post)
admin.site.register (comment , admin_com)
