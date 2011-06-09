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


from django.shortcuts import render_to_response as rtr
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from models import questionCategories
from models import questions
from forms import AskForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _


@login_required
def show_category(req):
    FaqCategory = questionCategories.objects.all()
    return rtr ('faq_categories.html',{'Items' : FaqCategory })

@login_required
def show_questions(req,categoryId):
    FaqQuestionsPublic = questions.objects.filter(category = categoryId , public = True)
    FaqQuestionsPrivate = questions.objects.filter(category = categoryId , user = req.user)
    return rtr ('faq_questions.html',{'Public' : FaqQuestionsPublic , 'Private' : FaqQuestionsPrivate })

@login_required
def show_detail(req,questionId):
    FaqQuestion = questions.objects.filter(id == questionId)
    return rtr ('faq_detail.html',{'Items' : FaqQuestion })

@csrf_protect
@login_required
def ask (req):
    a = User.objects.get (username=req.user)
    
    if req.method == "POST":
        f = AskForm (req.POST)
        if f.is_valid():
            questions.title = request.POST['title']
            question.question = req.POST['question']
            questions.save(req.user)
            return rtr("faq.html",{"message":_('Thanks for your contact we will answer you soon'),"f":f}, context_instance=RequestContext(req))
        else:
            return rtr("faq_ask.html",{"error":_('Please fill in the blanks'),"f":f}, context_instance=RequestContext(req))
    else:
        f = AskForm ()
        return rtr("faq_ask.html",{"f":f})
