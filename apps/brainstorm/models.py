from django.db import models
from django.utils.translation import ugettext as _





class category (models.Model):
    title = models.CharField ( max_length = 30 , verbose_name =  _("Title") )
    published = models.BooleanField ( default = False , verbose_name =  _("Publish"))
    
    def __unicode__ (self):
        return self.title

    class Meta:
        verbose_name_plural = _('Category')

class storm (models.Model):
    email = models.EmailField (verbose_name =  _("Email"))
    title = models.CharField ( max_length = 100 , verbose_name =  _("Title") )
    category = models.ForeignKey ('category' , verbose_name =  _("Category"))
    description = models.TextField (verbose_name =  _("Description"))
    
    

    def __unicode__ (self):
        return self.title

    class Meta:
        verbose_name_plural = _('Storm')

class comment (models.Model):
    email = models.EmailField (verbose_name =  _("Email"))
    storm = models.ForeignKey ('storm' , verbose_name =  _("Storm"))
    comment = models.TextField (verbose_name =  _("Comment"))
    
    def __unicode__ (self):
        return self.comment

    class Meta:
        verbose_name_plural = _('Comment')










        
