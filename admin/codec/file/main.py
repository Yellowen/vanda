import os
import shutil


class codec (object):
    """
    file protocol codec.
    """
    def __init__ (self):
        pass


    def getFile (self , src , dst):
        """
        Get src file and copy that to dst
        """
        shutil.copy ( src[7:] , dst)
