from django.conf import settings
from django.views.generic import base

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
    WorkDetailAPIView
    )

from itez.authentication.viewsets import (
    RegisterViewSet,
    LoginViewSet,
    ActiveSessionViewSet,
    LogoutViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
    *router.urls,
]

router.register(
    "register", 
    RegisterViewSet, 
    basename="register"
    )
router.register(
    "login", 
    LoginViewSet, 
    basename="login"
    )
router.register(
    "checkSession", 
    ActiveSessionViewSet, 
    basename="check-session"
    )
router.register(
    "logout", 
    LogoutViewSet, 
    basename="logout"
    )
router.register(
    "edit", 
    UserViewSet,
    basename="user-edit"
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
