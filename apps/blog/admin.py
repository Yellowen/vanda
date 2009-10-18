from django.contrib import admin
from models import *

class admin_entry (admin.ModelAdmin):
    list_display = ["title"  , "datetime" , "author" , "text"]
    #+++ month and year filter should add too by adding some methods to entry model
    #--- datetime filter should remove in future
    list_filter = ["datetime" , "author" ]
    search_field = [ "title" , ]



admin.site.register (entry , admin_entry)
