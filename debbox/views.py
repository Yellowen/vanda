from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from core.log import logger


def tmpindex(request):
    logger.info("adasdasdasd")
    return HttpResponse("It Works huuuuuuuuuuuuray")


@login_required
def dashboard(request):
    """
    User Dashboard. index page for Debbox.
    """
    return HttpResponse("It Works huuuuuuuuuuuuray")
