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
    dpm.Update ()
    dpm.List ()
    pkg = []
    for i in  range (1 ,12):
        pkg.append ({"id" : i , "checked" : "checked"})
        
    return rr ('admin/dpm/pkglist.html' , {"pkg" : pkg})
    
