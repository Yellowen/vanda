from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from models import Post


class LatestPosts (Feed):
    feed_type = Rss201rev2Feed
    title = "Lastest logs from lxsameer"
    link = "/links/"
    description = "Lastest logs from lxsameer(all posts)"

    def items(self):
        return Post.objects.order_by('-datetime')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
