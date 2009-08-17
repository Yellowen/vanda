from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class Installer (models.Model):
    # here i should add the help text if i succeed.
    File = models.FileField (_("File") , help_text=_("Upload and install a package") ,  upload_to = 'tmp/')
    class Meta:
        verbose_name_plural = _('Installer')
        


class application (models.Model):
    Name = models.CharField (max_length = 50,  unique = True , verbose_name = _('Name') )
    # each application identify it self by SHA1 hash.
    # i should find a better way
    SHA1 = models.CharField (max_length = 40 , unique = True ,editable = False , verbose_name = _('SHA1 hash') , help_text = _("Each application identify it self by its SHA1 hash"))
    Author = models.CharField (max_length = 30 , verbose_name = _('Author'))
    Email = models.EmailField (verbose_name = _('Email'))
    Home = models.URLField (blank = True , verbose_name = _('Home Page') )
    url = models.CharField (max_length = 50 , help_text = _("Enter a url that you want to application handle that") , verbose_name = _('Url'))
    Description = models.TextField (blank = True , verbose_name = _('Description')  )
    Publish = models.BooleanField (default = True , verbose_name = _('Publish'))
    

    def __unicode__ (self):
        return self.Name

    class Meta :
        verbose_name_plural = _('Applications')
        

