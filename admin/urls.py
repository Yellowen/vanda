from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
                       (r'^$', pkgm_mng),
                       (r'^installer/([A-Za-z]*)/$', installer),
                       (r'^installer/$', installer, {'param' :None}),
)
