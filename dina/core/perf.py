import time
from dina.log import Logger

class ExecTime (object):
    """
    ExecTime is a decorator that measure the execution
    time of a function and helps in the code optimization
    process.
    """

    def __init__ (self, function):

        self.f = function
        self.logger = Logger (self.f.__name__)
        
    def __call__ (self, *args):
        a = time.time ()
        result = self.f(*args)
        b = time.time ()
        self.logger.info ("Execute in : %s seconds." % (b - a))
        return result
