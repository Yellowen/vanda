# -----------------------------------------------------------------------------
#    Vanda dashbord - Dashboard application of Vanda platform
#    Copyright (C) 2012  Sameer Rahmani <lxsameer@gnu.org>
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
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


@login_required
def index(request):
    """
    Dashboard index.
    """
    return rr("dashboard/index.html",
              {},
              context_instance=RequestContext(request))


@login_required
def tmp_index(request):
    """
    Dashboard temporary index.
    """
    return rr("dashboard/tmp/index.html",
              {},
              context_instance=RequestContext(request))
