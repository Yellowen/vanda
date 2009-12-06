

def dassert ( test_str ):
    from django.conf import settings
    if settings.DEBUG:
        print test_str
