from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin



urlpatterns = patterns('',
                       (r'brainstorm/' , include ('apps.brainstorm.urls')),
                       (r'pages/' , include ('dina.fem.page.urls')),
                       (r'blog/' , include ('apps.blog.urls')),
                       
)
