from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin



urlpatterns = patterns('',
                       (r'^$' , 'apps.brainstorm.views.show'),
                       (r'([1-9]{1,3})/comments/$' , 'apps.brainstorm.views.comments'),
                       (r'category/$' , 'apps.brainstorm.views.new_cat'),
                       
)
