from django.contrib import admin
from django.contrib.auth.models import User
from itez.beneficiary.models import (
    Province,
    District,
)

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
