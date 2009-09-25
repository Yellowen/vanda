from django.shortcuts import render_to_response as rr
import DPM
# Create your views here.



def pkgm_mng (request):
    return rr ('admin/dpm.html')


def installer (requst , param):
    if param == "desc" :
        return rr ('admin/dpm.html')
    else:
        return rr ('admin/dpm/installer_ui.html')


def installer_test (request ):
    dpm = DPM.DPM ()
    dpm.update ()
    pkg1 = dpm.pkglist ()
    pkg = list ()
    for i in  pkg1:
        m = i.split ("::")[1]
        if m == "*":
            check = "checked"
        else:
            check = ""
        pkg.append ({"id" : i , "checked" : check , "name" : i.split("::")[0]})
        
    return rr ('admin/dpm/pkglist.html' , {"pkg" : pkg})
    
