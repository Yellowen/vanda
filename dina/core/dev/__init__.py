

def dassert ( test_str ):
    from django.conf import settings
    import sys
    if settings.DEBUG and 'runserver' in sys.argv:
        print test_str
