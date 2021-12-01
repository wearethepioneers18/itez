# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from itez.beneficiary import views

urlpatterns = [

    # The home page
    path("", views.index, name='home'),
    path("events", views.user_events, name='user_events'),
    
    path("report", views.beneficiary_report, name='report'),
    path("list_beneficiary/", views.BeneficiaryListView.as_view(), name='list_beneficiary'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
