from django.contrib import admin
from itez.beneficiary.models import (
    Province,
    District,
    Permission
)

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Permission, PermissionAdmin)