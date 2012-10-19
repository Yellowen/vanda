# -----------------------------------------------------------------------------
#    Vanda - Web development platform
#    Copyright (C) 2011 Some Hackers In Town
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

import json

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from models import City


def state(request, state_id):
    """
    return a json of a state_id.
    """
    try:
        cities = City.objects.filter(state__id=state_id)
        res = {"status": "0",
               "cities": list()}
        append = res["cities"].append
        for city in cities:
            append((city.id, city.name))
        return HttpResponse(json.dumps(res))

    except City.DoesNotExist:
        res = {"status": "-1",
               "msg": _("There is no such state."),
               }
        return HttpResponse(json.dumps(res))
