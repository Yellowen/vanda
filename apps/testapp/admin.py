from django.contrib import admin
from models import *
class A (admin.ModelAdmin):
    pass


admin.site.register (test , A)
