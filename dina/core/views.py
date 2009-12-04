from django.shortcuts import render_to_response as rr
from django.http import HttpResponse as HR

from django.contrib.auth.decorators import user_passes_test
import DPM

# Create your views here.


@user_passes_test(lambda u: u.is_superuser , login_url='/admin/')
def pkgm_mng (request):
    return rr ('admin/dpm.html')

@user_passes_test(lambda u: u.is_superuser , login_url='/admin/')
def installer (requst ):
    
        return rr ('admin/dpm/installer_ui.html' )


@user_passes_test(lambda u: u.is_superuser , login_url='/admin/')
def desc (requst , item):
    
        dpm = DPM.DPM ()
        dic = dpm.show (item)
        return HR ('<p>' + dic["short"] + '</p>')
    



@user_passes_test(lambda u: u.is_superuser)
def installer_test (request ):
    dpm = DPM.DPM ()
    dpm.update ()
    pkg1 = dpm.pkglist ()
    pkg = list ()
    a = 1
    for i in  pkg1:
        m = i.split ("::")[5]
        if m == "*":
            check = "checked"
        else:
            check = ""
        if (a % 2) == 0 :
            pkg.append ({"id" : i.split("::")[1] , "checked" : check , "name" : i.split("::")[0] , "version" : i.split("::")[2] , "short_desc" :  i.split("::")[4] , "color" : "a"})
        else:
            pkg.append ({"id" : i.split("::")[1] , "checked" : check , "name" : i.split("::")[0] , "version" : i.split("::")[2] , "short_desc" :  i.split("::")[4]})
        a += 1
    return rr ('admin/dpm/pkglist.html' , {"pkg" : pkg})
    
@user_passes_test(lambda u: u.is_superuser , login_url='/admin/')
def apply (request):
    if request.method == "POST":
        pkglist = list ()
        for i in request.POST:
            pkglist.append (i)

        dpm = DPM.DPM ()
        #+++ a removal test should come here
        dpm.install (pkglist)
        return HR (a)
