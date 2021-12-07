# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from itez.beneficiary import views

app_name = "beneficiary"

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("events", views.user_events, name="user_events"),
    path("uielements", views.uielements, name="uielements"),
    path("report", views.beneficiary_report, name="report"),
    path("beneficiary/list", views.BenenficiaryListView.as_view(), name="list"),
    path("beneficiary/create", views.BeneficiaryCreateView.as_view(), name="create"),
    path(
        "beneficiary/<int:pk>/detail",
        views.BeneficiaryDetailView.as_view(),
        name="details",
    ),
    path(
        "beneficiary/export_beneficiary_data",
        views.export_beneficiary_data,
        name="export_beneficiary_data",
    ),
    path(
        "beneficiary/poll_async_results/<task_id>",
        views.poll_async_resullt,
        name="export_beneficiary_data",
    ),
    path(
        "beneficiary/<int:pk>/medical_record_list",
        views.MedicalRecordListView.as_view(),
        name="medical_record_list",
    ),
    # Medical Record `beneficiary:medical_record_list`
    path(
        "medical_record_list",
        views.MedicalRecordListView.as_view(),
        name="medical_record_list",
    ),
    path(
        "medical_record/<int:pk>/details",
        views.MedicalRecordDetailView.as_view(),
        name="medical_record_detail",
    ),
    path(
        "medical_record_create",
        views.MedicalRecordCreateView.as_view(),
        name="medical_record_create",
    ),
]
