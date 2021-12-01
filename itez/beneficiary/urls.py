# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from itez.beneficiary import views

urlpatterns = [

    # The home page
    path("", views.index, name='home'),
    path("events", views.user_events, name='user_events'),
    path("uielements", views.uielements, name='uielements'),
    
    path("report", views.beneficiary_report, name='report'),
    path("list_beneficiary", views.list_beneficiary, name='list_beneficiary'),
    path("medical_record", views.MedicalRecordCreateView.as_view(), name='medical_record'),
    path("<int: beneficiary_id>/medical_record_list", views.MedicalRecordListView.as_view(), name='medical_record_list'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
