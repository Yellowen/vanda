import os
import shutil
import random
import simplejson as json
from django.conf import settings
from Repository import *
from models import Repository as rp

class DPMError (Exception):
    def __init__ (self , err):
        self.errstr = err
    def __unicode__ (self):
        return self.errstr
    def __str__ (self):
        return self.errstr




class DPM (object):
    """
    Dina Package manager.
    """
    
    def __init__ (self ):
        
        # Setting up cache directory path
        if settings.DPM_CACHE :
            if settings.DPM_CACHE[-1] != "/":
                self.cache = settings.DPM_CACHE + "/"
            else:
                self.cache = settings.DPM_CACHE
        else:
            self.cache = '/tmp/'

        self.id = random.randrange (100 ,200)

        confs = rp.objects.all ()
        self._repositories = self._sourceparser (confs)
        


    def _sourceparser (self , conflist):
        """
        Parse the source list for repositories.
        """

        #+++ may be i write a better parser
        repos = list ()
        for i in conflist:
            
            url =i.url.split (' ')[0]
            try:
                codename = i.url.split (' ')[1]
            except:
                codename = "stable"
            sections =i.url.split (' ')[2:]
            repos.append (Repository (url , codename , sections))
        return repos



    def List (self , section="all"):
        """
        Return the packages list in given category.
        """
        for i in self._repositoris:
            try:
                fd = open (self.cache + "repos/"  + i.name + "/Packages.json", 'r' )
                pkgs = json.loads (fd.read())
                
                
        pkgfile = self._getFile (
    



    def Install (self , pkglist):
        """
        Installer a Package list.
        """

        # Checking for other DPM process by lock file
        try:
            fd = open (self.cache + "lock"  , 'r')
            oid = fd.read ()
            fd.close ()
            raise DPMError ("An other DPM process with '%s' ID running." % (oid))
        except:
            fd = open (self.cache + "lock"  , 'w')
            fd.write (str (self.id))
            fd.close ()

        

    
        
        

