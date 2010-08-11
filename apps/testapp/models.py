from django.db import models
from dina.conf.base import ConfigBase
class test (models.Model):
    name = models.CharField (max_length=30)


class config (ConfigBase):
    active = models.BooleanField ()
    name = models.CharField (max_length=30)
    
