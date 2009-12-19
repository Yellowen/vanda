from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin



urlpatterns = patterns('',
                       (r'brainstorm/$' , 'apps.brainstorm.views.show'),
                       
)
