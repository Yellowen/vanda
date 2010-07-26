from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class questionCategories (models.Model):
    name  = models.CharField (verbose_name=_('Question category title')max_length = 100)
    description = models.TextField(verbose_name=_('Question category description'),null=True, blank=True)
    image = models.ImageField(verbose_name=_('Question category image'),height_field=None, width_field=None,max_length="7000",upload_to="uploads/faq_category/")
       
    def __unicode__(self):
        return "%s" % self.name 
