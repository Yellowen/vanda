from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.


class menu (models.Model):
    title = models.CharField (max_length = 30 , verbose_name = _("Title"))
    submenus = models.ManyToManyField ('self' , verbose_name = _("Submenus") , symmetrical=False , blank= True)
    items = models.ManyToManyField ('item' , verbose_name = _('items') , symmetrical=False , blank = True)
    #location
    weight = models.IntegerField (max_length = 2 , verbose_name = _("Weight") , default = 0 , help_text = _("A menu with the lower weight value will stay in top. (Not in Shamsiel WebDesk.)"))
                                  
    root = models.BooleanField (default = False , verbose_name = _("Root Menu ?"))
                                  
    def __unicode__ (self):
        return self.title


class item (models.Model):
    title = models.CharField (max_length = 30 , verbose_name = _("Title"))
    url = models.CharField (max_length = 100 , verbose_name = _("Target"))
    #newwindow
    weight = models.IntegerField (max_length = 2 , verbose_name = _("Weight") , default = 0 , help_text = _("A menu with the lower weight value will stay in top. (Not in Shamsiel WebDesk.)"))
    def __unicode__ (self):
        return self.title
