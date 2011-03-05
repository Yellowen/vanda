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
from models import menu
from models import item
from django.utils.translation import ugettext as _


class menu_admin (admin.ModelAdmin):
    # by setting fieldsets we decide to how should admin create section for this model look like
    fieldsets = (
         (None, {
            'fields': (('title' , 'parent'), ('items' , 'publish'),)
        }),
         (_('Advance'), {
            'classes': ('collapse',),
            'fields': (('view' , 'mclass') ,) 
        }),


         )     

class item_admin (admin.ModelAdmin):
    pass


admin.site.register (menu , menu_admin)
admin.site.register (item , item_admin)
