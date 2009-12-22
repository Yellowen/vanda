from django.contrib import admin
from models import *
from django.utils.translation import ugettext as _



class page_admin (admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title' , 'slug' )
    #+++ i should add an user name in list display
    list_display = ('title' , 'slug' , 'home' , 'published' , 'get_absolute_url' , 'date')
    list_filter = ('published' , )
    # by setting fieldsets we decide to how should admin create section for this model look like
    fieldsets = (
         (None, {
            'fields': (('title' , 'slug'), 'content' , ('published' , 'home'), )
        }),
         
         )
    def save_model (self, request, obj, form, change):
        if obj.home == True:
            a = page.objects.filter ( home = True).update (home = False)
            
        obj.save ()

    
        
admin.site.register (page , page_admin)


