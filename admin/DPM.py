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
            repos.append (Repository (url , self.cache , codename , sections ))
        return repos




    def Update (self , repo='all'):
        """
        Update the Packages file of given repository. and cache the packages file
        """
        for i in self._repositories:
            if repo == 'all':
                i.update ()
            else if repo == i.name:
                i.update ()
                
        pkgs = list ()
        for i in self._repositories:
            addr = self.cache + "repo/" + i.name
            dirs = os.listdir ( addr )
            for j in dirs:
                if j[0] == '.':
                    pass
                else:
                    fd = open (addr + "/" + j + "/Packages.json")
                    jobj = json.loads (fd.read ().lower ())
                    fd.close ()
                    tmppkgs = dict ()

                    for y in jobj :
                        #+++ here i should add extra dara this is just for basic usage
                        pname = y["package"]
                        phash = y["hash"]
                        pversion = y["version"]
                        if tmppkgs.has_key (phash):
                            pass
                        else:
                            tmppkgs[phash] = pname  + "::" + phash + "::" + pversion


                    
                        
        






    def List (self , section="all"):
        """
        Return the packages list in given category.
        """
        repos = list()
        for i in self._repositoris:
            try:
                fd = open (self.cache + "repos/"  + i.name + "/Packages.json", 'r' )
                pkgs = json.loads (fd.read())
                repos.append ({"name" : i.name , "pkglist" : pkgs})
                for j in pkgs:
                    if pkglist.has_key (j["Package"]):
                        

                
                
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

        

    
        
        

