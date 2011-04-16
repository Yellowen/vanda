from django.conf.urls.defaults import patterns

from debbox.core.vpkg.debcover import discovery


urlpatterns = patterns('',
    # Login url
    (r'^login/$',
     'debbox.core.auth.views.Login'),

    # Logout url
    (r'^logout/$', 'debbox.core.auth.views.Logout'),

    (r'^$', 'views.dashboard'),
)

discovery.url_patterns()
print "<>><<<<>>>>> ", discovery.urls

