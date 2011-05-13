from django.conf.urls.defaults import patterns

from debbox.core.logging import logger
from vpkg.discover import ApplicationDiscovery


discovery = ApplicationDiscovery(logger=logger)

urlpatterns = patterns('',
    # Login url
    (r'^login/$',
     'debbox.core.auth.views.Login'),

    # Logout url
    (r'^logout/$', 'debbox.core.auth.views.Logout'),
)

urlpatterns += discovery.url_patterns()
