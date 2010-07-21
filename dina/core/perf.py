from timeit import Timer
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


        t = Timer(stmt=self.f(*args))
        try:
            self.logger.info ("execution time : %s" % t.timeit())
        except:
            t.print_exc()

