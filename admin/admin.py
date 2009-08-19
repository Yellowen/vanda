from django.contrib import admin
from models import *
from django.conf import settings
import installer
import os 
from django.core.management import call_command


class inst_admin (admin.ModelAdmin):
    # overriding the save_model of our model
    def save_model (self , request , obj , fro , change):
        # save the model and file will uploaded
        
        obj.save ()
        # getting the file address
        package_address = settings.MEDIA_ROOT + "/" + str (obj.File)
        
        # delete the uploaded file and installer database entry
        ins = installer.installer (package_address)
        app = ins.install ()
        app.save ()

        obj.delete ()
        


class app_admin (admin.ModelAdmin):
    list_display = ('Name' , 'Version' , 'SHA1' , 'Author' , 'Email' , 'Home' , 'url' , 'Publish')
    list_display_links = ('Name' , 'Publish' , )
    list_filter = ('Publish' , )
    list_per_page = 15
    ordering = ('Name' , )
    search_fields = ('Name' ,)
    
    #+++ here i should add some ACTION about publishing 

    #+++ i should find a better way to deal with dynamic apps ------------
    def save_model (self , request , obj , fro , change):
        #if obj.Publish == True :
        #    # I use app name as it conf file name 
        #    fd = open (settings.FS_ROOT + "/confs/" + str(obj.Name) + ".conf" , 'w')
        #    fd.write ('apps.' + str(obj.Name) + "\n")
        #    fd.write (str(obj.url) + "\n")
        #    fd.close ()
        #else :
        #    os.unlink (settings.FS_ROOT + "/confs/" + str(obj.Name) + ".conf")
        obj.save ()
        installer.get_apps ()
        #call_command ('sqlall' , 'news')
        call_command ('syncdb')
        
        
    #------------------------------------------------------------------


    def delete_view (self , request , obj , fro , change):
        pass
        

admin.site.register (Installer , inst_admin)
admin.site.register (application , app_admin)
