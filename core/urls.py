from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
                       (r'^$', pkgm_mng),

                       (r'^installer/test/$', installer_test),
                       (r'^installer/([A-Za-z0-9]{40})/$', desc),                       
                       (r'^installer/$', installer),

                       )
