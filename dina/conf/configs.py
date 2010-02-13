


class ConfigBase (type):
    """
    Meta class for all configuration classes.
    """
    
    
    def __new__ (cls , name ,bases , attrs):
        """
        Target configuration instance build here.
        """
        
        super_new = super(ConfigBase , cls).__new__
        
        print "Name: %s" % name
        print "Base Classes:"
        for i in bases:
            print "\t%s" % i
        
        for i in attrs.keys ():
            print "%s = %s" % (i , type(attrs[i]).__name__)
            
        new_class = super_new (cls , name , bases , attrs )
        setattr(new_class , "sameer" , "rahmani")
        return new_class
        
        




class Config (object) :
    """
    Dina Configuration framework base class.
    """
    
    # Dina build a configuration interface for an application with
    # a class that inherit from this class in the app source code
    # and registered with dina.conf.register
    #
    # The config class can override completely ( view , url and ...)
    
    
    __metaclass__ = ConfigBase
    
    
    
    def __init__ (self):
        pass
    
    def __getattribute__ (self , name):
        #object.__getattribute__ (self , name)
        #print " = ".join (name)
        return object.__getattribute__ (self , name)
            
    def __setattr__ (self , name , value):
        print " = ".join (name,value)
        self.__dict__[name] = int (value ) + 1 