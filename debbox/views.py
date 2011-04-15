from django.shortcuts import render_to_response as rr
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


@login_required
def dashboard(request):
    """
    User Dashboard. index page for Debbox.
    """
    return rr("dashboard.html", {},
              context_instance=RequestContext(request))
