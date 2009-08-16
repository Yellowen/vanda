from django.contrib import admin
from models import *

class inst_dmin (admin.ModelAdmin):

    def save_model (self , request , obj , from , change):
        pass
    
        

admin.site.register (Installer)
admin.site.register (application)
