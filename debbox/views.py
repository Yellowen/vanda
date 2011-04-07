from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from debbox.core.logging.instance import logger


def tmpindex(request):
    logger.info("adasdasdasd")
    return HttpResponse("It Works huuuuuuuuuuuuray")
# ISSUE : It is better to use phrases with meaning in logger.info and HttpResponse

@login_required
def dashboard(request):
    """
    User Dashboard. index page for Debbox.
    """
    logger.info("here")
    return HttpResponse("It Works huuuuuuuuuuuuray")
# ISSUE : It is better to use phrases with meaning in logger.info and HttpResponse
