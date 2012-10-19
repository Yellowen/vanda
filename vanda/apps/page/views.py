# -----------------------------------------------------------------------------
#    Vanda page application
#    Copyright (C) 2010-2012 Sameer Rahmani <lxsameer@gnu.org>
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

from django.shortcuts import render_to_response as rr
from django.http import Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from django.conf import settings

from models import Page


def show_page(request, slug):
    """
    show the page with the given slug
    """
    lang = settings.LANGUAGE_CODE

    site = request.META["HTTP_HOST"]
    try:
        current_site = Site.objects.get(domain=site)
    except Site.DoesNotExist:
        raise Http404("Wrong site")

    try:
        page = Page.objects.get(slug=slug,
                                site=current_site,
                                language=lang,
                                publish=True)

    except Page.DoesNotExist:
        raise Http404("Wrong page")
    return rr("page.html",
              {"page": page,
               "title": "%s | %s" % (_(settings.TITLE), page.title)},
              context_instance=RequestContext(request))
