from django.shortcuts import render_to_response as rr
from django.contrib.auth.decorators import user_passes_test
from models import *
# Create your views here.


#+++ TODO: add permission checker for menu editing
@user_passes_test(lambda u: u.is_superuser , login_url='/admin/')
def change_list (request):
    root_menus = menu.objects.filter (parent = None)
    return rr ('admin/change_tree.html')
