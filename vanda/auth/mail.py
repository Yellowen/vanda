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
from django.core.urlresolvers import reverse


BODY = """
Hi $USERNAME$!

Welcome to $TITLE$. In order to activate your new account,
please click the URL below.

http://$LINK$

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

    def __init__(self, user, code, domain):

        body = BODY
        body = body.replace("$USERNAME$", user.username)
        body = body.replace("$TITLE$", domain)
        body = body.replace("$EMAIL$", settings.SUPPORT_MAIL)

        url = reverse('auth.views.verificate_email', args=[code])
        link = "%s%s" % (domain, url)

        body = body.replace("$LINK$", link)

        subject = "Email address verification"
        from_ = settings.SMTP_FROM

        super(VerificationMail, self).__init__(subject, body, from_,
                                               [user.email, ])
