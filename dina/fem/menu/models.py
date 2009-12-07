# Any time during the development process please read the brainstorm and goal files of this section and
# stay update with it , don't forget to review changelog of project ;)

from django.db import models
from django.utils.translation import ugettext as _

from  dina import mptt


class menu (models.Model):
    title = models.CharField (max_length = 30 , verbose_name = _("Title"))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    items = models.ManyToManyField ('item' , blank = True)

    

    def __unicode__ (self):
        return self.title


class item (models.Model):
    title = models.CharField (max_length = 30 , verbose_name = _("Title"))
    url = models.CharField (max_length = 100 , verbose_name = _("Target"))
    #newwindow

    weight = models.IntegerField (max_length = 2 , verbose_name = _("Weight") , default = 0 , help_text = _("A menu with the lower weight value will stay in top. (Not in Shamsiel WebDesk.)"))
    publish = models.BooleanField (default = False , verbose_name = _("Should it be piblished?"))
    def __unicode__ (self):
        return self.title



mptt.register (menu)
