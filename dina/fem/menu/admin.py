from django.contrib import admin
from models import *
from django.utils.translation import ugettext as _



class menu_admin (admin.ModelAdmin):
    # by setting fieldsets we decide to how should admin create section for this model look like
    fieldsets = (
         (None, {
            'fields': (('title' , 'parent'), ('items' , 'publish'), )
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


