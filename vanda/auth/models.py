# -----------------------------------------------------------------------------
#    Vanda - Web development platform
#    Copyright (C) 2011 Some Hackers In Town
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

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


# verification codes will expire after 2 days
VERIFICATION_TIME_LIMIT = 2


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"),
                             unique=True)

    def __unicode__(self):
        return "%s profile" % self.user

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


class Verification(models.Model):

    code = models.CharField(max_length=40,
                            verbose_name=_("Code"),
                            unique=True)
    user = models.ForeignKey(User, verbose_name=_("User"),
                             unique=True)
    date = models.DateTimeField(auto_now=True,
                                auto_now_add=True,
                                verbose_name=_("Sent Date"))

    def __unicode__(self):
        return self.code

    def create_verification_code(self):
        """
        create a verification code for self.user and return it
        """
        import hashlib
        from datetime import datetime

        from django.db import transaction

        m = hashlib.sha1()
        if self.user:
            m.update("%s%s" % (self.user.username, datetime.now()))
            hash_ = m.hexdigest()
            self.code = hash_

            with transaction.commit_on_success():
                Verification.delete_expired_codes()
                self.save()

            return hash_
        else:
            raise self.UserNotSet()

    def is_valid(self):
        """
        Return false if current activation code expired.
        """
        from datetime import datetime, timedelta

        expdate = datetime.now() - timedelta(days=VERIFICATION_TIME_LIMIT)
        if self.date < expdate:
            return False
        else:
            return True

    @staticmethod
    def delete_expired_codes():
        """
        Delete all the records with expired date.
        """
        from datetime import datetime, timedelta

        expdate = datetime.now() - timedelta(days=VERIFICATION_TIME_LIMIT)
        expired_codes = Verification.objects.filter(date__lt=expdate)
        expired_codes.delete()

    class UserNotSet(Exception):
        pass

    class Meta:
        verbose_name = _("Verification")
        verbose_name_plural = _("Verifications")
