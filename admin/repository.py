import codec
import os
import shutil


class RepositoryError (Exception):
    def __init__ (self , err):
        self.errstr = err
    def __unicode__ (self):
        return self.errstr
    def __str__ (self):
        return self.errstr
    


class Repository (object):
    """
    Dina Repository Class
    """

    def __init__ (self, url , codename="stable" , sections=["main",] ):
        self.protocol = url.split (':')[0]
        self.codec = codec.getCodec (self.protocol)
        if not self.codec :
            raise RepositoryError ("\"%s\" does not support by DPM at this time." % (self.protocol))
        self.codename = codename
        self.sections = sections
        if url[-1] == "/":
            url = url[:-1]
        self.url = url
        self.name = url.replace (' ' , '_').replace ('/' , '_')
        
        

    def _setUrl (self , url):
        #+++ i should add here an url validation
        self.url = url
        

    def _getUrl (self):
        return self.url
    
    url = property (fget = _getUrl , fset= _setUrl)


    def _getFile (self , addr):
        """
        Download the given file.
        """
        if not addr:
            return -1
        filename = addr.split ('/')[-1]
        try:
            fd = open (self.cache + filename , 'r')
        except:
            try:
                self.codec.getFile (self.url + addr , self.cache)
                fd = open (self.cache + filename , 'r')
            except:
                #+++ here i should add better output
                raise RepositoryError ("codec.getFile : error")
        fd.close ()
        return self.cache + filename
        
            
            


    def getPackages_List (self , section="all"):
        """
        Return all packages in given category.
        """
        try:
            fd = open (self.cache + "repos/"  + 
        pkgfile = self._getFile (
        
