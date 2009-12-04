from django.shortcuts import render_to_response as rr
from django.template import Context , Template
from django.contrib.auth.decorators import user_passes_test
from models import *
# Create your views here.



def gentree (x):
    tree = "<li><a href='/admin/menu/menu/%d/'>%s</a><ul>\n" % (x.id , x)
    for i in x.get_children ():
        tree = tree +  gentree (i)
    
    for i in x.items.filter (publish = True):
        tree = tree + "<li><a href='/admin/menu/item/%d/'>%s</a></li>\n" % (i.id , i)
    tree = tree + "</ul></li>\n"
    return tree
    


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


