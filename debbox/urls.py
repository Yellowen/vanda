from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
    # Login url use Django default login view
    (r'^login/$',
     'django.contrib.auth.views.login',
     {'template_name': 'auth/login.html'}),

    # Logout url use Django default logout view
    (r'^logout/$', 'django.contrib.auth.views.logout'),

    (r'^$', 'views.dashboard'),
)
