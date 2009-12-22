from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin



urlpatterns = patterns('',
                       #+++ i should use named group url instead of normal one
                       (r'([^/]+)/$' , 'dina.fem.page.views.show_page'),
                       
                       
)
