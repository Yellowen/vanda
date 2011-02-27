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
from models import contact


class admin_category (admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ["title"  , "published" , "category_order" , "description",]
    list_filter = ["category_order" , "title" , "published" , ]
    search_field = [ "title" , ]

class admin_contact (admin.ModelAdmin):
    fieldsets = (
        ('Necessary information', {
            'fields': ('name', 'slug', 'published', 'contact_order' , 'category_id' ,'author')
        }),
        ('Optional information', {
            'classes': ('collapse',),
            'fields': ('contact_position', 'email', 'street_address' ,'town' ,'state' ,'postalcode' ,'tell' ,'cell' ,'fax' ,'weburl' ,'miscellaneous' )
        }),
        ('Optional parameter view', {
            'classes': ('collapse',),
            'fields': ('contact_position_flag', 'email_flag', 'street_address_flag' ,'town_flag' ,'state_flag' ,'postalcode_flag' ,'tell_flag' ,'cell_flag' ,'fax_flag' ,'weburl_flag' ,'miscellaneous_flag' )
        }),
    )

    
    
admin.site.register (category ,admin_category )
admin.site.register (contact ,admin_contact )
