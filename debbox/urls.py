from django.conf.urls.defaults import patterns

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.tmpindex'),
    # (r'^admin/', include(admin.site.urls)),
)
