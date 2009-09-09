import os
import tarfile
import shutil
import random
from models import *
from django.db.models.signals import post_delete 
from django.conf import settings



class installer (object):
    """ Dina Installer main class """
    
    # this class will extract and install an application or a template package
    def __init__ (self , file_path):
        self.path = file_path
        


    def _extract (self):
        """ Extract the archive file in the same directory  """

        #!!! Here i should add error handling

        # Get the current working directory address
        pwd = os.getcwd ()
        self.return_path = pwd
        os.chdir ('/tmp/')

        # build a random unique name
        dirname = 'dina_' + str (random.randrange (1 , 1000))
        self.dirname = dirname

        # build a dir
        os.mkdir(dirname)

        # Copy archive and its meta data to /tmp
        shutil.copy2 (self.path , '/tmp/' + dirname + "/tmp_archive")

        # Change the current working directory to /tmp
        os.chdir ('/tmp/' + dirname)

        #extract the file name from path
        archive =  "tmp_archive"#self.path.split('/')[-1]
        
        # open archive file for extraction
        tar = tarfile.open (archive)

        # extract the archive file
        tar.extractall ()
        tar.close ()


    def _read_index (self):
        """ Read the package information file """
        
        # pars the information file to a python dictionary
        dic = self._parser ('package.info')
        

        #+++ here i should add an exception handler --------------
        #+++ here i should add an sha1 validator 
        if dic["type"].lower ()  == "application":

            self.obj = application (Name = dic["name"])
            self.obj.url = dic["url"]

        elif dic["type"].lower () == "template":

            self.obj = template (Name = dic["name"])
            self.obj.Default = False
            #+++ here i should add the difference field
        
        self.obj.Version = dic["version"]
        self.obj.SHA1 = dic["sha1"]
        self.obj.Author = dic["author"]
        self.obj.Email = dic["email"]
        self.obj.Home = dic["home"]
        
        self.obj.Description = dic["description"]
        
        self.obj.Publish = False
        #------------------------------------------------------

        return 0
    


    def install (self):
        """ install the package """

        self._extract ()
        self._read_index ()
        
        os.chdir ('/tmp/' + self.dirname)


        # Installing application
        if self.obj.type == "application":

            target_dir = settings.APP_ROOT
        else:
            target_dir = settings.TEMPLATE_DIRS

        shutil.copytree (self.obj.Name , target_dir + "/" + self.obj.Name)
        os.rmdir ('/tmp/' + self.dirname)
        os.chdir (self.return_path)
        
        return self.obj
        
            
            

    def _parser (self , file):
        """Parse the file to a python dictionary"""
        #+++ here i should add a conf validator
        #+++ here i should add a ; for end of line
        try:
            fd = open (file , "r")
            lines = fd.readlines ()
            fd.close ()
        except:
            print "Error: The file %s does not exists or permission denid !" % (file)
            return -1
        dic = {}
        for i in lines:
            if i[0] != '#':
                
                li = i.split ("=")
                dic[li[0].lower().strip()] = li[1].lower().strip()
                
        return dic






#+++ may be i should put this in a class


#+++ add an error handler here    
def update_apps ():
    papp = application.objects.filter (Publish=True)
    
    iapp = ()
    appurl = ()
    for i in papp:
        iapp += ('apps.' + str (i.Name) , )
        appurl += (("r'"+ str(i.url ) + "' , 'apps."  + str(i.Name) + ".urls'" ) , )
    settings.INSTALLED_APPS += iapp
        
    os.unlink (settings.FS_ROOT + "/confs/__init__.py")
    print appurl
    fd = open (settings.FS_ROOT + "/confs/__init__.py" , 'w')
    
    #fd.write ('from django.conf.urls import defaults\n\n')
    fd.write ('published_apps = ' + str (iapp).replace (',' , ' , \n'))
    fd.write ("\n\n")
    fd.write ("urls = [")
    if len(papp) != 0 :
        
        for i in appurl:
            print i 
            fd.write ("[" + i+  "] , ")
    #else:
    #    fd.write ("published_url = defaults.patterns ('' , " + str (appurl).replace ('"' , '') )
    fd.write ("\n]")
    fd.close ()
    
    #fd = open (settings.FS_ROOT + "/confs/urls.py" , 'w')
    #fd.write (" ," .join (appurl).replace ('"' , ''))
    #fd.close ()
    return 
    
def app_update_callback (sender , **keyword):
    update_apps ()


post_delete.connect (app_update_callback , sender=application)
