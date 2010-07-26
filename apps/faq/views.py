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

from django.forms import ModelForm
from django.shortcuts import render_to_response as rtr
from django.http import Http404 , HttpResponseRedirect  , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.forms import ModelForm
from models import *
from forms import AskForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _

@login_required
def show_category(req):
    FaqCategory = questionCategories.objects.all()
    return rtr ('faq_categories.html',{'Items' : FaqCategory })
