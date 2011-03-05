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
from models import page
from models import section
from django.utils.translation import ugettext as _


media = '/media'
class page_admin (admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title' , 'slug')
    #+++ i should add an user name in list display
    list_display = ('title', 'category' , 'slug' , 'home' , 'published' , 'get_absolute_url' , 'date')
    list_filter = ('published' ,)
    list_editable = ('published' ,)
    # by setting fieldsets we decide to how should admin create section for this model look like
    fieldsets = (
         (None, {
            'fields': ('category', ('title' , 'slug'), 'content' , ('published' , 'home'),)
            
         , 'description' : _("Here you can build pages for fron view.") }),
         
         )
    class Media:
        js = (media + '/js/jquery.js', media + '/js/wymeditor/jquery.wymeditor.js', media + '/js/htmleditor.js')
    def save_model (self, request, obj, form, change):
        if obj.home == True:
            a = page.objects.filter (home=True).update (home=False)
            
        obj.save ()


class section_admin (admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title' , 'slug')
    #+++ i should add an user name in list display                                                                          
    list_display = ('title' , 'slug', 'published' , 'get_absolute_url')
    list_filter = ('published' ,)
    list_editable = ('published' ,)
    # by setting fieldsets we decide to how should admin create section for this model look like                            
    fieldsets = (
         (None, {
            'fields': (('title' , 'slug'), 'description' , ('published'), 'image',)
         }),)
    class Media:
        js = (media + '/js/jquery.js', media + '/js/wymeditor/jquery.wymeditor.js', media + '/js/htmleditor.js')



class category_admin (admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title' , 'slug')
    #+++ i should add an user name in list display                                                                          
    list_display = ('section' , 'title' , 'slug', 'published' , 'get_absolute_url')
    list_filter = ('published' ,)
    list_editable = ('published' ,)
    # by setting fieldsets we decide to how should admin create section for this model look like                            
    fieldsets = (
         (None, {
            'fields': ('section' , ('title' , 'slug'), 'description' , ('published'), 'image',)
         }),)
    class Media:
        js = (media + '/js/jquery.js', media + '/js/wymeditor/jquery.wymeditor.js', media + '/js/htmleditor.js')


    
        
admin.site.register (page , page_admin)
admin.site.register (section , section_admin)
admin.site.register (category , category_admin)


