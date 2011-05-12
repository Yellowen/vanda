from django.conf.urls.defaults import patterns

from django.conf.settings import discovery


urlpatterns = patterns('',
    # Login url
    (r'^login/$',
     'debbox.core.auth.views.Login'),

    # Logout url
    (r'^logout/$', 'debbox.core.auth.views.Logout'),
)

urlpatterns += discovery.url_patterns()
