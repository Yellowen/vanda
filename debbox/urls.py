from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
    # Login url
    (r'^login/$',
     'debbox.core.auth.views.Login'),

    # Logout url
    (r'^logout/$', 'debbox.core.auth.views.Logout'),

    (r'^$', 'views.dashboard'),
)
