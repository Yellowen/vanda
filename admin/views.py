from django.shortcuts import render_to_response as rr
# Create your views here.



def pkgm_mng (request):
    return rr ('admin/dpm.html')


def installer (requst , param):
    if param == "desc" :
        return rr ('admin/dpm.html')
    else:
        return rr ('admin/dpm/installer_ui.html')


