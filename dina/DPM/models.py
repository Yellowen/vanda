import os
import shutil

from django.db import models

from django.conf import settings
from django.utils.translation import ugettext as _

from managers import TemplateManager

# From old version (0.1.0) -------------------------------------------------------------------
# This model will be rreplaced in the future by DPM
class application (models.Model):

    Name = models.CharField (max_length = 50,  unique = True , verbose_name = _('Name') )

    # each application identify it self by SHA1 hash.
    
    Version = models.CharField (max_length = 15 , verbose_name = _('Version'))

    SHA1 = models.CharField (max_length = 40 , unique = True ,editable = False
                             , verbose_name = _('SHA1 hash') , 
                             help_text = _("Each application identify it self by its SHA1 hash"))

    Author = models.CharField (max_length = 30 , verbose_name = _('Author'))
    Email = models.EmailField (verbose_name = _('Email'))
    Home = models.URLField (blank = True , verbose_name = _('Home Page') )
    url = models.CharField (max_length = 50 , 
                            help_text = _("Enter a url that you want to application handle that") ,
                            verbose_name = _('Url'))

    Description = models.TextField (blank = True , verbose_name = _('Description')  )
    Publish = models.BooleanField (default = True , verbose_name = _('Publish'))
    

    def delete (self):

        shutil.rmtree (settings.FS_ROOT + '/apps/' + str (self.Name))
        super (application , self).delete ()
        

    def __unicode__ (self):
        return self.Name

    class Meta :
        verbose_name_plural = _('Applications')
        


#---------------------------------------------------------------------------





# This Model will be replace or modified by DPM in the future version
class Template (models.Model):
    """
    Dina Template class each template will have an entry here
    that make it easy to manage them.
    """
    
    Name = models.CharField (max_length = 30,  unique = True , verbose_name = _('Template Name') )
    SHA1 = models.CharField (max_length = 40, unique = True , verbose_name = _("SHA1"), blank=True , null=True)
    Author = models.CharField (max_length = 30 , verbose_name = _('Author') , blank=True , null=True)
    Email = models.EmailField (verbose_name = _('Email')  , blank=True , null=True )
    Home = models.URLField ( verbose_name = _('Home Page')  , blank=True , null=True)
    Description = models.TextField ( verbose_name = _('Description') , blank=True , null=True )
    # TODO: unique=True should add to Active field
    Active = models.BooleanField ( verbose_name = _('Active'))

    # Set the default manager . Since TemplateManager class extend the Manager class
    # all of default manager's method will be available.
    objects = TemplateManager ()

    def delete (self):
        # TODO: Checking for a global setting that allow to run a hook inside of templates
        # in the installation and deletation time.

        # TODO: Remove the template directory and its media and its model.

        pass


    def save (self, force_insert=False, force_update=False):
        if self.Active:
            try:
                a = Template.objects.get (Active=True)
                a.Active = False
                a.save ()
            except Template.DoesNotExist:
                pass
            
        super(Template, self).save (force_insert, force_update)
        
    def install (self):
        # TODO: Checking for a global setting that allow to run a hook inside of templates
        # in the installation and deletation time.

        # TODO: Read the template default path , and copy the template files and media

        pass
        
    def __unicode__ (self):
        return self.Name

    class Meta :
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        permissions = (
            ('can_add_template' , _("Can add template.")),
            ('can_edit_template' , _("Can edit template.")),
            ('can_edit_template_source' , _("Can edit template source.")),
            ('can_delete_template' , _("Can delete template.")),
            )


# This Model will be replace or modified by DPM in the future version
class Repo (models.Model):
    url = models.CharField (max_length=100, unique=True , verbose_name=_('url') , help_text = _("Url should be in '[protocol]://[address]/ [codename] [section] [section] ... format"))
    comment = models.TextField(blank=True , verbose_name = _('comment'))

    def __unicode__ (self):
        return self.url

    def __str__ (self):
        return self.url
