from models import Page
from django.shortcuts import render_to_response as rtr

def view_page(request, page_name):
    try:
        page = Page.objects.get(pk=page_name)
    except Page.DoesNotExist:
        return rtr("create.html",{"page_name"},page_name)
