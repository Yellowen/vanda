from django.shortcuts import render_to_response as rr
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.template import RequestContext
from django.conf import settings

from forms import ContactUs


def index(request):
    if request.method == 'POST':
        form = ContactUs(request.POST)
        if form.is_valid():
            send_mail('User Contact', form.cleaned_data['message'],
                      form.cleaned_data['email'],
                      settings.ADMINS_MAIL)
            SentMessage = _('Your message has been sent successfully!')
            return rr('msg.html', {'msg': SentMessage})
        else:
            return rr('contact_us.html', {'ContactUs': form},
                      context_instance=RequestContext(request))
    else:
        form = ContactUs()
        return rr('contact_us.html', {'ContactUs': form},
                  context_instance=RequestContext(request))