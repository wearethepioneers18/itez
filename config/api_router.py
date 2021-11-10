from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from itez.users.api.views import UserViewSet, ChangePasswordView
from itez.beneficiary.api.views import (
    AgentDetailAPIView,
    BeneficiaryAPIView,
    BeneficiaryParentAPIView,
    ProvinceAPIView,
    DistrictAPIView,
    ServiceAreaAPIView,
    WorkDetailAPIView
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


router.register("users", UserViewSet)
router.register("users/change_password", ChangePasswordView)
router.register("agents", AgentDetailAPIView)
router.register("beneficiaries", BeneficiaryAPIView)
router.register("beneficiary_parents", BeneficiaryParentAPIView)
router.register("provinces", ProvinceAPIView)
router.register("districts", DistrictAPIView)
router.register('service_area', ServiceAreaAPIView)
router.register('work_detail', WorkDetailAPIView)

app_name = "api"
urlpatterns = router.urls
