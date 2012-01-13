# -----------------------------------------------------------------------------
#    Ultra Blog - Data type base blog application for Vanda platform
#    Copyright (C) 2011 Sameer Rahmani <lxsameer@gnu.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.comments.signals import comment_was_posted
from django.conf import settings

from base import Post
from config import Setting


class PostModerator(CommentModerator):
    email_notification = True


def on_comment_was_posted(sender, comment, request, *args, **kwargs):

    from django.contrib.sites.models import Site
    from django.conf import settings

    try:
        from ultra_blog.akismet import Akismet
    except ImportError:
        return

    apikey = Setting.get_setting("spam_apikey")
    if apikey:
        if Setting.get_setting("antispam") == "0":
            ak = Akismet(
                key=apikey,
                blog_url='http://%s/' % request.META["HTTP_HOST"]
                )
            ak.baseurl = 'api.antispam.typepad.com/1.1/'
        else:
            ak = Akismet(
                key=apikey,
                blog_url='http://%s/' % request.META["HTTP_HOST"]
                )

        if ak.verify_key():
            data = {
                'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referrer': request.META.get('HTTP_REFERER', ''),
                'comment_type': 'comment',
                'comment_author': comment.user_name.encode('utf-8'),
                }

            if ak.comment_check(comment.comment.encode('utf-8'),
                            data=data, build_data=True):
                comment.flags.create(
                    user=comment.content_object.author,
                    flag='spam'
                    )
                comment.is_public = False
                comment.save()

    try:
        from core.websucks.unix import UnixClient

        print ">>> ", dir(comment)
        if comment.is_public == True:
            send_dict = {"model": comment.content_object.__class__.__name__,
                         "content": comment.comment,
                         "user": comment.user_name,
                         "object_id": str(comment.object_pk),
                         "date": comment.submit_date.strftime("%H:%M %d %b %Y")}
            UnixClient(settings.UNIX_SOCKET).send(send_dict, event="new_comment")
            
    except ImportError:
        return


moderator.register(Post, PostModerator)
comment_was_posted.connect(on_comment_was_posted)
