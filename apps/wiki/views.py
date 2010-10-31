from models import Page
from django.shortcuts import render_to_response as rtr
from django.http import HttpResponseRedirect

import markdown


def search_page(request):
    if request.method == "POST":
        f = SearchForm(request.POST)
        if not f.is_valid():
            return rtr("search.html",{"form":f})
        else:
            pages = Page.objects.filter(name__contains = f.cleaned_data["text"])
            return rtr("search.html", {"form":f,"pages":pages})
    f = SearchForm()
    return rtr("search.html", {"form":f})

specialPages = {"SearchPage":search_page}
def view_page(request, page_name):
    if page_name in specialPages:
        return specialPages[page_name](request)
    try:
        page = Page.objects.get(pk=page_name)
    except Page.DoesNotExist:
        return rtr("create.html",{"page_name":page_name})
    content = page.content
    return rtr("view.html",{"page_name":page_name, "content":markdown.markdown(content)})

def edit_page(request, page_name):
    try:
        page = Page.objects.get(pk=page_name)
        content = page.content
    except Page.DoesNotExist:
        content = ""
    return rtr("edit.html",{"page_name":page_name,"content":content})

def save_page(request, page_name):
    content = request.POST["content"]
    try:
        page = page.objects.get(pk=page_name)
        page.content = content
    except Page.DoesNotExist:
        page = Page(name=page_name, content=content)
    page.save()
    return HttpResponseRedirect("/wiki/" + page_name + "/")

