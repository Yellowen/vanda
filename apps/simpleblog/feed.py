from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.translation import ugettext as _

from models import *


class LatestPosts (Feed):
    feed_type = Rss201rev2Feed
    title = _("Lxsameer's weblog feeds")
    link = "/blog/"
    description = _("Recent logs form lxsameer")

    def items(self):
        return Post.objects.order_by('-datetime')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
