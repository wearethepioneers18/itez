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
