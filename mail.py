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

from django.conf import settings
from django.core.mail import EmailMessage


BODY = """
Hi $USERNAME$!

Welcome to $TITLE$. In order to activate your new account,
please click the URL below.

$LINK$

If the above URL does not work try copying and pasting it into your browser.
If you continue to have problem please feel free to contact us.

Best regards,
The $TITLE$ staff
$EMAIL$
"""


class VerificationMail(EmailMessage):
    """
    Verification Mail class handling verification mail sending.
    """

    subject = "Email address verification"
    mail = settings.SMTP_FROM
    body = BODY

    def __init__(self, user, code, domain):
        self.user = user
        self.code = code
        self.domain = domain

    def send(self, fail_silently=False):
        """
        Send the verification mail.
        """
        self.body = self.body.replace("$USERNAME$", self.user.username)
        self.body = self.body.replace("$TITLE$", self.domain)
        self.body = self.body.replace("$EMAIL$", settings.SUPPORT_MAIL)

        url = ""
        link = "%s/%s" % (self.domain, url)
