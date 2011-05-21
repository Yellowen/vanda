from base import SectionNode, ItemNode


LOADING = False


def autodiscover():
    """
    Load the Dashboard class of the given application and return an instance.
    application should be a pythonic path to a application.

    This function will look for a dashboard module inside the application and
    a Dashboard class inside the module.
    """

    global LOADING

    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            __import__(app)
            app_path = sys.modules[app].__path__
        except AttributeError:
            continue
        try:
            imp.find_module('dashboard', app_path)
        except ImportError:
            continue
        __import__("%s.dashboard" % app)
        app_path = sys.modules["%s.dashboard" % app]
    LOADING = False
