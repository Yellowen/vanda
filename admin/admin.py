from django.contrib import admin
from models import *
import tarfile
from django.conf import settings
import installer

class inst_admin (admin.ModelAdmin):
    # overriding the save_model of our model
    def save_model (self , request , obj , fro , change):
        # save the model and file will uploaded
        obj.save ()
        # getting the file address
        package_address = settings.MEDIA_ROOT + "/" +  str (obj.File)
        # delete the uploaded file and installer database entry
        obj.delete ()
        

admin.site.register (Installer , inst_admin)
admin.site.register (application)
