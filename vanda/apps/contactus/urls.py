from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
        (r'^$', 'vanda.apps.contactus.views.index'),
)
