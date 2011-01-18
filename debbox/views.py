from django.http import HttpResponse

from core.log import logger


def tmpindex(request):
    logger.info("adasdasdasd")
    return HttpResponse("It Works huuuuuuuuuuuuray")
