from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from itez.beneficiary.api.views import (
    DrugAPIView,
    LabAPIView,
    PrescriptionAPIView,
    FacilityAPIView,
    FacilityTypeAPIView,
    ImplementingPartnerAPIView,
    ServiceAPIView,
    ServiceProviderPersonelAPIView,
    ServiceProviderPersonelQualificationAPIView
)

urlpatterns = [

    path("index", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    
    # User management
    path("users/", include("itez.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),

   # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path("", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Additional APIViews
    path(
        "lab/", 
        LabAPIView.as_view(), 
        name='lab'
        ),
    path(
        "drug/", 
        DrugAPIView.as_view(), 
        name='drug'
        ),
    path(
        "service/", 
        ServiceAPIView.as_view(), 
        name='service'
        ),
    path(
        "facility/", 
        FacilityAPIView.as_view(), 
        name='facility'
        ),
    path(
        "prescription/", 
        PrescriptionAPIView.as_view(), 
        name='prescription'
        ),
    path(
        "facility_type/", 
        FacilityTypeAPIView.as_view(), 
        name='facility_type'
        ),
    path(
        "implementing_partner/", 
        ImplementingPartnerAPIView.as_view(), 
        name='implementing_partner'
        ),
    path(
        "service_provider_personnel/", 
        ServiceProviderPersonelAPIView.as_view(), 
        name='service_provider_personnel'
        ),
    path(
        "service_provider_personnel_qualification/", 
        ServiceProviderPersonelQualificationAPIView.as_view(), 
        name='service_provider_personnel_qualification'
        )    
]

admin.site.site_header = "ITEZ"                   
admin.site.index_title = "Data management of Intersex and Trans-persons in Zambia."                 
admin.site.site_title = "ITEZ Administration" 

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
