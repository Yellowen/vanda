from django.conf.urls.defaults import patterns

from vpkg import vpkg

from debbox import dashboard

dashboard.autodiscover()


urlpatterns = patterns('',
    # Login url
    (r'^login/$',
     'debbox.core.auth.views.Login'),

    # Logout url
    (r'^logout/$', 'debbox.core.auth.views.Logout'),
)

urlpatterns += vpkg.url_patterns()
