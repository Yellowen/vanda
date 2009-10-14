from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.
class entry (models.Model):
    """
    Entry model that hold posts
    """
    title = models.CharField (max_length=20 , verbose_name=_("Title"))
    author = models.ForeignKey ("auth.User" , editable = False , verbose_name = _("Author"))
    datetime = models.DateTimeField (auto_now_add = True , editable=False , verbose_name = _('Date and Time'))
    text = models.TextField (verbose_name = _('Text'))
    def __unicode__ (self):
        return self.title 
    class Meta:
        verbose_name_plural = _("Entries")
        verbose_name = _('Entry')

class comment (models.Model):
    """
    Comment model hold the comments of posts.
    """

    author = models.ForeignKey ("auth.User" , editable=False , verbose_name = _("Author"))
    datetime = models.DateTimeField (auto_now_add = True , editable=False , verbose_name = _('Date and Time'))
    text = models.TextField (verbose_name = _('Text'))
    post = models.ForeignKey ("entry" , verbose_name = _("Post"))
    
    def __unicode__ (self):
        return self.text

    class Meta:
        verbose_name_plural = _("Comments")
        verbose_name = _('Comment')

