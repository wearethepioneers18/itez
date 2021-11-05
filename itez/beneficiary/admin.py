from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from itez.beneficiary.models import (
    Province,
    District,
    ServiceArea,
    WorkDetail,
    AgentDetail,
    Beneficiary,
    BeneficiaryParent
)


class BeneficiaryAdmin(OSMGeoAdmin):
    list_display = [
        "first_name",
        "last_name",
        "beneficiary_ID",
        "created",
        "parent_details"
    ]


class BeneficiaryParentAdmin(admin.ModelAdmin):
    list_display = [
        "father_first_name",
        "father_last_name",
        "mother_first_name", 
        "mother_last_name"
    ]

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]


class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]


class WorkDetailAdmin(admin.ModelAdmin):
    list_display = [
        "gross_pay",
        "company",
        "work_address",
        "insured",
    ]


class AgentDetailAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'birthdate',
        'agend_ID',
        'gender',
        'location'
    ]

admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(ServiceArea, ServiceAreaAdmin)
admin.site.register(AgentDetail, AgentDetailAdmin)
admin.site.register(WorkDetail, WorkDetailAdmin)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(BeneficiaryParent, BeneficiaryParentAdmin)
