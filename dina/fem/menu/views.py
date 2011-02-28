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



from django.shortcuts import render_to_response as rr
from django.template import Context , Template
from django.template.loader import get_template
from django.contrib.auth.decorators import user_passes_test
from models import menu
# Create your views here.



def gentree (x):
    # get the jstree template in 'admin/menu/tree_view.html' 
    t = get_template ('admin/menu/tree_view.html')
    con = {"obj" : x , "submenus" : "" , "items" : []}
    # define res as a Safestring
    res = Template ('').render (Context ())
    for i in x.get_children ():
        res = res +  gentree (i)
    
    for i in x.items.all ():
        con["items"].append (i)
    if res:
        con["submenus"] = Context (res)
    return t.render (Context (con))
    


#+++ TODO: add permission checker for menu editing
@user_passes_test(lambda u: u.is_superuser , login_url='/admin/')
def change_list (request):
    root_menus = menu.objects.filter (parent = None)
    tree = "<ul>\n"
    for i in root_menus:
        tree = tree + gentree (i)
    tree = tree + "</ul>\n"
    t = Template (tree)
    return rr ('admin/change_tree.html', {"msg" : "Menu View" , "app_label" : "Menu" ,"tree" : t.render (Context ())})
