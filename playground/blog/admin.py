# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
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
# ---------------------------------------------------------------------------------


from django.contrib import admin
from models import category
from models import post


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


    
class admin_category(admin.ModelAdmin):
    pass

admin.site.register(category, admin_category)
admin.site.register (post , admin_post)