from django.contrib import admin
from itez.beneficiary.models import (
    Province,
    District,
    ServiceArea,
    WorkDetail,
    AgentDetail,
    Beneficiary,
    BeneficiaryParent,
    Facility,
    FacilityType,
    ImplementingPartner,
    ServiceProviderPersonel,
    ServiceProviderPersonelQualification
)


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "beneficiary_id",
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
        'agent_id',
        'gender',
        'location'
    ]


class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

class FacilityAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'facility_type',
        'implementing_partner'
    ]


class ImplementingPartnerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'ip_type'
    ]
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'qualification',
        'department',
        'facility'
    ]

class ServiceProviderPersonelQualificationAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(ServiceArea, ServiceAreaAdmin)
admin.site.register(AgentDetail, AgentDetailAdmin)
admin.site.register(WorkDetail, WorkDetailAdmin)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(BeneficiaryParent, BeneficiaryParentAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(FacilityType, FacilityTypeAdmin)
admin.site.register(ImplementingPartner, ImplementingPartnerAdmin)
admin.site.register(ServiceProviderPersonel, ServiceProviderAdmin)
admin.site.register(ServiceProviderPersonelQualification, ServiceProviderPersonelQualificationAdmin)
