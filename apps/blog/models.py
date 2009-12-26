from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class post (models.Model):
    """
    Entry model that hold posts
    """
    title = models.CharField (max_length=20 , verbose_name=_("Title"))
    slug = models.SlugField (max_length=20 , verbose_name=_("Slug") , help_text = _("This field will fill automaticly by title field."))
    author = models.ForeignKey ("auth.User" , editable = False , verbose_name = _("Author"))
    datetime = models.DateTimeField (auto_now_add = True , editable=False , verbose_name = _('Date and Time'))
    text = models.TextField (verbose_name = _('Text'))
    
    def __unicode__ (self):
        return self.title
    def get_absolute_url (self):
        return "/blog/post/%s" % self.slug
    
    class Meta:
        verbose_name_plural = _("Posts")
        verbose_name = _('Post')

