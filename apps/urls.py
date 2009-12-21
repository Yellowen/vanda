from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin



urlpatterns = patterns('',
                       (r'brainstorm/$' , 'apps.brainstorm.views.show'),
                       (r'brainstorm/([1-9]{1,3})/comments/$' , 'apps.brainstorm.views.comments'),
                       (r'brainstorm/category/$' , 'apps.brainstorm.views.new_cat'),
                       
)
