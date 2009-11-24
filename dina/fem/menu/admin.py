from django.contrib import admin
from models import *



class menu_admin (admin.ModelAdmin):
    pass

class item_admin (admin.ModelAdmin):
    pass


admin.site.register (menu , menu_admin)
admin.site.register (item , item_admin)


