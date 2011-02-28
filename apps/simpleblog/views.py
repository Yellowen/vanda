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


from django.shortcuts import render_to_response as rr
from django.template import RequestContext
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from decorators import check_auth
from models import Category
from models import Comment
from models import Post
from models import Setting
from forms import CommentForm


def blog_index(req):
    # TODO: add a filter to retrive last month posts only
    post_list = Post.objects.all().order_by('-datetime')
    ppp = 10
    setting = Setting.configs()
    if setting.post_per_page:
        ppp = setting.post_per_page
    paginator = Paginator(post_list, ppp)
    try:
        page = int(req.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return rr('blog.html', {"posts": posts})


def post_view (request, slug_):
    
    post = Post.objects.get (slug=slug_)
    comments_list = post.comments ()
    cpp = 10
    setting = Setting.configs ()
    if setting.comment_per_page:
        cpp = setting.comment_per_page
        
    paginator = Paginator(comments_list, cpp)
    
    try:                                                                                                                                                   
        page = int(request.GET.get('page', '1'))                                                                                                           
    except ValueError:                                                                                                                                     
        page = 1                                                                                                                                       
        
    try:                                                                                                                                                   
        comments = paginator.page(page)                                                                                                                
    except (EmptyPage, InvalidPage):                                                                                                                       
        comments = paginator.page(paginator.num_pages)                                                                                                 
                                                             
    return rr ('post_view.html', {"post" : post, 'comments' : comments})


@check_auth
def post_comment (request, slug):
    if request.method == "POST":
        form = CommentForm (request.POST)
        
        if form.is_valid ():
            post = Post.objects.get (slug=slug)
            com = Comment (nick=form.cleaned_data['nick'],\
                           post=post,\
                           content=form.cleaned_data['comment'])
            com.save ()
            return HttpResponseRedirect ('/blog/post/%s' % slug)
        
        else:
            form = CommentForm (request.POST)
            return rr ('comment_form.html', {'form' : form},\
                       context_instance=RequestContext(request))

    else:
        form = CommentForm ()
        # TODO: add latest comment to bottom of view
        return rr ('comment_form.html', {'form' : form},\
                   context_instance=RequestContext(request))


def category_index(req, slug_):
    # TODO: add a filter to retrive last month posts only
    category = Category.objects.get(slug=slug_)
    post_list = category.post_set.all().order_by('-datetime')
    ppp = 10
    setting = Setting.configs()
    if setting.post_per_page:
        ppp = setting.post_per_page
    paginator = Paginator(post_list, ppp)
    try:
        page = int(req.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return rr('blog.html', {"posts": posts})
