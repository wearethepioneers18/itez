from django.contrib import admin
from itez.beneficiary.models import Province

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

admin.site.register(Province, ProvinceAdmin)