# Any time during the development process please read the brainstorm and goal files of this section and
# stay update with it , don't forget to review changelog of project ;)

from django.db import models
from django.utils.translation import ugettext as _

class page (models.Model):
    title = models.CharField (max_length = 30 , verbose_name = _("Title") , help_text = _("Title will show as page <title> tag."))
    slug = models.SlugField (verbose_name = _("Slug") , help_text = _("This field will fill automaticly by title.") , unique = True)
    content = models.TextField (verbose_name = _("Body") , help_text = _("HTML allowed."))
    date = models.DateTimeField(db_index=True, auto_now_add=True)
    published = models.BooleanField (verbose_name = _("Publish ?") )
    home = models.BooleanField (verbose_name = _("Shall it be home page ?") , help_text = _("Only one page can be the home page at a time.")  )

    def __unicode__ (self):
        return self.title

    
    def get_absolute_url (self):
        return "/page/%s/" % self.slug
