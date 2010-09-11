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
        try:
            self.logger = Logger (self.f.__name__)
            self.__name__ = self.f.__name__
        except AttributeError:
            self.logger = Logger ("ExecTime: %s" % self.f)
            self.__name__ = self.f
        

        
    def __call__ (self, *args):
        
        a = time.time ()
        y = time.clock ()
        result = self.f(*args)
        z = time.clock ()
        b = time.time ()
        
        self.logger.debug ("Execute in : %s seconds. Process time: %s" % ((b - a), (z-y)))
        return result
