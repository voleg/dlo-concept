from django.contrib import admin

from minddistrict_connect.models import PlatformConfig, PlatformProfile
 

@admin.register(PlatformConfig, PlatformProfile)
class PlatformAdmin(admin.ModelAdmin):
    ...
