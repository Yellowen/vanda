from dina.log import Logger
import inspect

class RequestResponseDebug (object):
    """
    This is a middleware for debuging, this middleware log the url and it's
    responsible view to allow easier debug.
    """
    
    def __init__ (self):
        self.logger = Logger ("Debug Middleware")
        
    def process_request(self, request):
        return None
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        self.logger.debug ("URL: %s"% request.path)
        try:
            self.logger.debug ("View: %s at %s" % (view_func.__name__, inspect.getmodule(view_func)))
        except AttributeError:
            self.logger.debug ("View: %s at %s" % (view_func, inspect.getmodule(view_func)))
        return None
    
    def process_response(self, request, response):
        return response
    
    def process_exception(self, request, exception):
        return None
