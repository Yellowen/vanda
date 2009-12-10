from django.shortcuts import render_to_response as rr
from django.template import Context , Template
from django.template.loader import get_template
from django.contrib.auth.decorators import user_passes_test
from models import *
# Create your views here.



def gentree (x):
    # get the jstree template in 'admin/menu/tree_view.html' 
    t = get_template ('admin/menu/tree_view.html')
    con = {"title" : x.title , "submenus" : "" , "items" : []}
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


