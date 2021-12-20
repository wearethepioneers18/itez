from django.contrib import admin
from django.contrib.gis.db import models
from itez.beneficiary.models import (
    MedicalRecord,
    Lab,
    Drug,
    Province,
    District,
    Prescription,
    ServiceArea,
    WorkDetail,
    Agent,
    Beneficiary,
    BeneficiaryParent,
    Facility,
    FacilityType,
    ImplementingPartner,
    Service,
    ServiceProviderPersonel,
    ServiceProviderPersonelQualification,
)

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from mapwidgets.widgets import GooglePointFieldWidget


class LabResource(resources.ModelResource):
    class Meta:
        model = Lab


@admin.register(Lab)
class LabAdmin(ImportExportModelAdmin):
    resource_class = LabResource

    list_display = ("title", "requested_date")

    search_fields = (
        "title",
        "facility__name",
        "beneficiary__beneficiary_id",
    )


class DrugResource(resources.ModelResource):
    class Meta:
        model = Drug


@admin.register(Drug)
class DrugAdmin(ImportExportModelAdmin):
    resource_class = DrugResource

    list_display = ("name", "manufacturer", "expiry_date")

    search_fields = (
        "name",
        "beneficiary__beneficiary_id",
    )


class PrescriptionResource(resources.ModelResource):
    class Meta:
        model = Prescription


@admin.register(Prescription)
class PrescriptionAdmin(ImportExportModelAdmin):
    resource_class = PrescriptionResource
    list_display = ("title", "date")

    search_fields = ("title",)


class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service


@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource

    list_display = (
        "title",
        "client_type",
        "service_type",
        "datetime",
    )


class FacilityResource(resources.ModelResource):
    class Meta:
        model = Facility


class BeneficiaryResource(resources.ModelResource):
    class Meta:
        model = Beneficiary


@admin.register(Beneficiary)
class BeneficiaryAdmin(ImportExportModelAdmin):
    resource_class = BeneficiaryResource

    list_display = [
        "beneficiary_id",
        "first_name",
        "last_name",
        "gender",
        "sex",
        "art_status",
        "hiv_status",
        "last_vl",
        "registered_facility",
        "phone_number",
        "email",
        "date_of_birth",
        "education_level",
        "created",
    ]
    search_fields = [
        "sex",
        "phone_number",
        "email",
        "beneficiary_id",
        "first_name",
        "last_name",
    ]


class BeneficiaryResource(resources.ModelResource):
    class Meta:
        model = Beneficiary


class BeneficiaryParentAdmin(admin.ModelAdmin):
    list_display = [
        "father_first_name",
        "father_last_name",
        "mother_first_name",
        "mother_last_name",
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


class AgentAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "birthdate",
        "agent_id",
        "gender",
        "location",
    ]
    formfield_overrides = {models.PointField: {"widget": GooglePointFieldWidget}}


class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Facility)
class FacilityAdmin(ImportExportModelAdmin):
    resource_class = FacilityResource
    list_display = ("name", "province", "district", "facility_type", "hmis_code")

    list_display_links = ("name",)
    search_fields = ("name", "hmis_code")

    list_filter = (
        "province",
        "facility_type",
        "district",
    )
    list_per_page = 30


class ImplementingPartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "ip_type"]


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "qualification",
        "department",
    ]


class ServiceProviderPersonelQualificationAdmin(admin.ModelAdmin):
    list_display = ["name"]


# register MedicalRecord class


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = [
        "beneficiary",
        "service",
        "prescription",
        "lab",
        "service_facility",
    ]

    list_filter = [
        "beneficiary",
        "service",
    ]
    list_per_page = 30


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(ServiceArea, ServiceAreaAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(WorkDetail, WorkDetailAdmin)
admin.site.register(BeneficiaryParent, BeneficiaryParentAdmin)
admin.site.register(FacilityType, FacilityTypeAdmin)
admin.site.register(ImplementingPartner, ImplementingPartnerAdmin)
admin.site.register(ServiceProviderPersonel, ServiceProviderAdmin)
admin.site.register(
    ServiceProviderPersonelQualification, ServiceProviderPersonelQualificationAdmin
)
