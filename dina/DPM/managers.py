from django.db import models


class TemplateManager (models.Manager):
    """
    This manager will add to template model and provide some functions like:
    setActive : this function the a template as active (template in use)
    """
    
    
    def setActive (self):
        """
        Set a template as active and deactivate lastest active template.
        """
        
        print str (self.get_query_set ())
        pass


    def getActiveTheme (self):
        """
        Return the current active themplate.
        """

        print str (self.get_query_set ())
        return super(TemplateMAnager , self).get_query_set ().get (Active=True)
