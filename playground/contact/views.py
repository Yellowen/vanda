# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
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
# ---------------------------------------------------------------------------------

from django.core.context_processors import csrf
from django.shortcuts import render_to_response as rr
from django.http import Http404
from django import forms
from models import category
from models import contact
from django.http import HttpResponseRedirect


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(max_length=1024,widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

def all_category_view (request):
    """
        Main view for all Contact category (This function will be show all category of contact)
    """
    ent = category.objects.all ().order_by("title")
    
    return rr ("category.html" , {"category" : ent})
 
def category_view (request, Slug):
    """
        Main view for Category (This function will be show all user in one category of contact)
    """
    try:
        Category_id = category.objects.get ( slug = Slug ).id
        ent = contact.objects.filter ( category_id = Category_id )
    except:
        return Http404 ()
    
    return rr ("category.html" , {"category" : ent})

def contact_view (request , Slug):
    """
        Sub view for Contact (This function will be show contact information and ...
    """
    try:
        contact_info = contact.objects.get( slug = Slug )
    except:
        return Http404 ()
    
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = [contact_info.email]
            if cc_myself:
                recipients.append(sender)

            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/') # Redirect after POST
    else: 
        form = ContactForm() # An unbound form
    ent = {"form" : form , "contact_info" : contact_info}
    ent.update(csrf(request))
    return rr ("contact.html" , ent)
        