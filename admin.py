from django.contrib import admin

from models import Verification, Profile


class ProfileAdmin(admin.ModelAdmin):
    pass


class VerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "date")
    search_fields = ("user", "code")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Verification, VerificationAdmin)
