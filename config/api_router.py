from django.conf import settings

from rest_framework.routers import DefaultRouter, SimpleRouter

from itez.users.api.views import (
    UserViewSet,
    ChangePasswordView,
    RoleAPIView
)
from itez.beneficiary.api.views import (
    AgentDetailAPIView,
    BeneficiaryAPIView,
    BeneficiaryParentAPIView,
    ProvinceAPIView,
    DistrictAPIView,
    ServiceAreaAPIView,
    WorkDetailAPIView,
    DrugAPIView,
    LabAPIView,
    PrescriptionAPIView,
    FacilityAPIView,
    FacilityTypeAPIView,
    ImplementingPartnerAPIView,
    ServiceAPIView,
    ServiceProviderPersonelAPIView,
    ServiceProviderPersonelQualificationAPIView,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register(
    "user", 
    UserViewSet
    )
router.register(
    "users/change_password", 
    ChangePasswordView
    )
router.register(
    "role", 
    RoleAPIView, 
    basename="role"
    )
router.register(
    "drug", 
    DrugAPIView, 
    basename='drug'
    )
router.register(
    "labs", 
    LabAPIView, 
    basename='lab'
    )
router.register(
    "prescription", 
    PrescriptionAPIView, 
    basename='prescriptions'
    )
router.register(
    "facility_type", 
    FacilityTypeAPIView, 
    )
router.register(
    "facility", 
    FacilityAPIView, 
    basename='facicility'
    )
router.register(
    "implementing_partner", 
    ImplementingPartnerAPIView, 
    basename='implementing_partner'
    )
router.register(
    "service", 
    ServiceAPIView, 
    basename='service'
    )
router.register(
    "service_provider_personnel", 
    ServiceProviderPersonelAPIView, 
    basename='service_provider_personnel'
    )
router.register(
    "service_provider_personnel_qualification", 
    ServiceProviderPersonelQualificationAPIView, 
    basename='service_provider_personnel_qualification'
    )
router.register(
    "agent", 
    AgentDetailAPIView
    )
router.register(
    "beneficiarie", 
    BeneficiaryAPIView
    )
router.register(
    "beneficiary_parent", 
    BeneficiaryParentAPIView
    )
router.register(
    "province", 
    ProvinceAPIView
    )
router.register(
    "district", 
    DistrictAPIView
    )
router.register(
    "service_area", 
    ServiceAreaAPIView
    )
router.register(
    "work_detail", 
    WorkDetailAPIView
    )

app_name = "api"
urlpatterns = router.urls
