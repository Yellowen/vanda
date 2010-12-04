from django.db import models
from dina.conf.models import Config


class test (models.Model):
    name = models.CharField (max_length=30)


class config (Config):
    active = models.BooleanField ()
    name = models.CharField (max_length=30)
    
