from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
    # Login url
    (r'^login/$',
     'debbox.core.auth.views.Login'),

    # Logout url use Django default logout view
    (r'^logout/$', 'django.contrib.auth.views.logout'),

    (r'^$', 'views.dashboard'),
)
