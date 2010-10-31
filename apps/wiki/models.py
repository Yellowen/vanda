from django.db import models

class Page(models.Model):
    name = modules.CharField(maxlength="20", primary_key=true)
    content = models.TextField(blank=True)
 

    # (r'^Dina/(?P<Page_name>[^/]+/edit/$', 'wikicamp.wiki.views.edit_page'),
