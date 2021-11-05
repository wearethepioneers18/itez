from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from itez.users.api.views import UserViewSet
from itez.beneficiary.api.views import (
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
router.register("provinces", ProvinceAPIView)
router.register("districts", DistrictAPIView)
router.register('service_area', ServiceAreaAPIView)
router.register('work_detail', WorkDetailAPIView)

app_name = "api"
urlpatterns = router.urls
