urlpatterns = patterns(
    'django.views.generic.list_detail',
    url(r'^product/$', 'object_list',
        {'queryset': Product.objects.all()}),
    url(r'^product/(?P<slug>[-\w]+)/$', 'object_detail',
        {'queryset': Product.objects.all()}))

