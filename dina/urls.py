from django.conf.urls.defaults import *
from django.contrib import admin
import os


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
  #  (r'^dpm/', include('dina.core.urls')),
    (r'^core/$', 'dina.core.views.pkgm_mng'),                   
    (r'^menu/menu/$', 'dina.fem.menu.views.change_list'),                   
    (r'^', include(admin.site.urls)),
                       
                       
)
