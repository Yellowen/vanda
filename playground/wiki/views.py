# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------

from django.shortcuts import render_to_response as rtr
from django.http import HttpResponseRedirect

import markdown

from forms import SearchForm
from models import Page


def search_page(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if not form.is_valid():
            return rtr("search.html", {"form": form})
        else:
            pages = Page.objects.filter(
                name__contains=form.cleaned_data["text"])
            contents = []
            if form.cleaned_data["search_content"]:
                contents = Page.objects.filter(
                    contents__contains=form.cleaned_data["text"])
            return rtr("search.html", {"form": form,
                                       "pages": pages,
                                       "contents": contents})
    form = SearchForm()
    return rtr("search.html", {"form": form})


specialPages = {"SearchPage": search_page}


def view_page(request, page_name):
    if page_name in specialPages:
        return specialPages[page_name](request)
    try:
        page = Page.objects.get(pk=page_name)
    except Page.DoesNotExist:
        return rtr("create.html", {"page_name": page_name})
    content = page.content
    return rtr("view.html", {"page_name": page_name,
                             "content": markdown.markdown(content)})


def edit_page(request, page_name):
    try:
        page = Page.objects.get(pk=page_name)
        content = page.content
    except Page.DoesNotExist:
        content = ""
    return rtr("edit.html", {"page_name": page_name,
                             "content": content})


def save_page(request, page_name):
    content = request.POST["content"]
    try:
        page = Page.objects.get(pk=page_name)
        page.content = content
    except Page.DoesNotExist:
        page = Page(name=page_name, content=content)
    page.save()
    return HttpResponseRedirect("/wiki/" + page_name + "/")
