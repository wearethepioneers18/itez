from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
    )

from itez.beneficiary.api.views import (
    DrugAPIView,
    FacilityAPIView,
    FacilityTypeAPIView,
    ImplementingPartnerAPIView,
    ServiceAPIView,
    ServiceProviderPersonelAPIView,
    ServiceProviderPersonelQualificationAPIView
)

urlpatterns = [

    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("itez.beneficiary.urls", namespace="beneficiary")),          
    path("", include("itez.authentication.urls")),
    path("", include("itez.users.urls", namespace="user")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "ITEZ Administration"                   
admin.site.site_title = "ITEZ Administration" 
admin.site.index_title = "Data management of Intersex and Trans-persons in Zambia."                 

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),

   # YOUR PATTERNS
    path('api/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path("api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Additional APIViews
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
