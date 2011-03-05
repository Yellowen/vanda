# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------------


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
        
        self.logger.debug ("Execute in : %s seconds. Process time: %s" % ((b - a), (z - y)))
        return result
