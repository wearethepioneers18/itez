# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from itez.beneficiary import views

app_name = "beneficiary"

urlpatterns = [
    path("", views.index, name="home"),
    path("events", views.user_events, name="user_events"),
    path("uielements", views.uielements, name="uielements"),
    path("report", views.beneficiary_report, name="report"),
    path("beneficiary/list", views.BenenficiaryListView.as_view(), name="list"),
    path("beneficiary/create", views.BeneficiaryCreateView.as_view(), name="create"),
    path("agent/list", views.AgentListView.as_view(), name="agent_list"),
    path("agent/create", views.AgentCreateView.as_view(), name="agent_create"),
    path(
        "agent/<int:pk>/detail",
        views.AgentDetailView.as_view(),
        name="agent_detail",
    ),
    path(
        "agent/<int:pk>/delete",
        views.agent_delete_view,
        name="agent_delete",
    ),
     path(
        "agent/<int:pk>/update",
        views.AgentUpdateView.as_view(),
        name="agent_update",
    ),
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
        views.poll_async_results,
        name="poll_async_results",
    ),
    path(
        "beneficiary/<int:id>/download_medical_report",
        views.medical_record_pdf,
        name="generate_medical_report",
    ),
    path(
        "beneficiary/<int:pk>/medical_record_list",
        views.MedicalRecordListView.as_view(),
        name="medical_record_list",
    ),
    path(
        "beneficiary/<int:pk>/delete",
        views.beneficiary_delete_view,
        name="delete",
    ),
    path(
        "beneficiary/<int:pk>/update",
        views.BeneficiaryUpdateView.as_view(),
        name="update",
    ),
    # Medical Record `beneficiary:medical_record_list`
    path(
        "medical_record/list",
        views.MedicalRecordListView.as_view(),
        name="medical_record_list",
    ),
    path(
        "medical_record/<int:pk>/details",
        views.MedicalRecordDetailView.as_view(),
        name="medical_record_detail",
    ),
    path(
        "beneficiary/<int:beneficiary_id>/medical_record/create",
        views.MedicalRecordCreateView.as_view(),
        name="medical_record_create",
    ),
]
