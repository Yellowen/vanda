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


import os

from django.contrib import admin
from models import *
from django.conf import settings
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


    #def add_view (self , request, form_url='', extra_context=None):
    #    pass
        


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
        
        
        
        obj.save ()
        
#        installer.update_apps ()
        call_command ('syncdb')
        
        
    #------------------------------------------------------------------

            
        
    


class temp_admin (admin.ModelAdmin):
    list_display = ('Name' , 'SHA1' , 'Author' , 'Email' , 'Home' , 'Active')
    list_display_links = ('Name',)
    list_editable = ('Active',)
    #list_filter = ('Publish' , )
    list_per_page = 15
    ordering = ('Name' , )
    search_fields = ('Name' ,)
    
    
    def save_model (self , request , obj , fro , change):
        

        obj.save ()
#        if obj.Active:
#            Template.objects.get (Active=True)
#            obj.objects.setActive (id=obj.id)

        


class repo_admin (admin.ModelAdmin):
    list_display = ('url' , 'comment')
    
        

#admin.site.register (Installer , inst_admin)
admin.site.register (application , app_admin)
admin.site.register (Template , temp_admin)
admin.site.register (Repo , repo_admin)

