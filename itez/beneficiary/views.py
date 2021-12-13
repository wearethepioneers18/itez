# -*- encoding: utf-8 -*-
import json
from django import template
from django.contrib.gis.db.models import fields
from django.db.models import query
from django.db.models import Q
from django.db.models.expressions import OrderBy
from django.db.models.functions.datetime import TruncMonth, TruncWeek, TruncDay
from django.views.generic import CreateView, FormView
from django.views.generic.detail import DetailView
from rolepermissions.roles import assign_role
from rolepermissions.roles import RolesManager
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from itez.beneficiary.models import GENDER_CHOICES, SEX_CHOICES
from rest_framework.filters import SearchFilter, OrderingFilter
import json


from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic import base

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from rolepermissions.roles import RolesManager
from django.conf import settings

from celery.result import AsyncResult
from itez import beneficiary

from itez.beneficiary.models import (
    Beneficiary,
    MedicalRecord,
    Province
)
from itez.beneficiary.models import Service
from django.db.models import Count
from django.db.models.functions import ExtractYear,ExtractWeek,ExtractMonth

from django.core.paginator import Paginator
from django.core.paginator import Paginator
from .tasks import generate_export_file

from itez.beneficiary.forms import BeneficiaryForm, MedicalRecordForm, AgentForm
from itez.beneficiary.models import Agent
from itez.users.models import User
from itez.beneficiary.models import Province

from .resources import BeneficiaryResource

from .resources import BeneficiaryResource
from .filters import BeneficiaryFilter


@login_required(login_url="/login/")
def index(request):
    opd = Service.objects.filter(client_type="OPD").count()
    hts = Service.objects.filter(service_type="HTS").count()
    vl = Service.objects.filter(service_type="VL").count()
    art = Service.objects.filter(client_type="ART").count()
    labs = Service.objects.filter(service_type="LAB").count()
    pharmacy = Service.objects.filter(service_type="PHARMACY").count()
    male = Beneficiary.objects.filter(gender="Male").count()
    female = Beneficiary.objects.filter(gender="Female").count()
    transgender = Beneficiary.objects.filter(gender="Transgender").count()
    other = Beneficiary.objects.filter(gender="Other").count()

    # Weekly Visits
    sun_day = MedicalRecord.objects.filter(interaction_date__week_day=1).count()
    mon_day = MedicalRecord.objects.filter(interaction_date__week_day=2).count()
    tue_day = MedicalRecord.objects.filter(interaction_date__week_day=3).count()
    wed_day = MedicalRecord.objects.filter(interaction_date__week_day=4).count()
    thu_day = MedicalRecord.objects.filter(interaction_date__week_day=5).count()
    fri_day = MedicalRecord.objects.filter(interaction_date__week_day=6).count()
    sat_day = MedicalRecord.objects.filter(interaction_date__week_day=7).count()

    uncleaned_user_roles = RolesManager.get_roles_names()
    cleaned_user_roles = []
    for user_role in uncleaned_user_roles:
        splitted_user_role = user_role.split("_")
        cleaned_user_role = " ".join(splitted_user_role).title()
        cleaned_user_roles.append({
            "key": f"{user_role}",\
            "value": f"{cleaned_user_role}"
        })
    gender_list = [gender[0] or gender[1] for gender in GENDER_CHOICES]
    sex_list = [sex[0] or sex[1] for sex in SEX_CHOICES]
    context = {
        "segment": "index",
        "opd": opd,
        "hts": hts,
        "vl": vl,
        "art": art,
        "labs": labs,
        "pharmacy": pharmacy,
        "male": male,
        "female": female,
        "transgender": transgender,
        "other": other,
<<<<<<< HEAD
        "sunday" : sun_day,
        "monday" : mon_day,
        "tuesday" : tue_day,
        "wednesday" : wed_day,
        "thursday" : thu_day,
        "friday" : fri_day,
        "saturday" : sat_day,
=======
        "sunday": sun_day,
        "monday": mon_day,
        "tuesday": tue_day,
        "wednesday": wed_day,
        "thursday": thu_day,
        "friday": fri_day,
        "saturday": sat_day,
        "user_roles": cleaned_user_roles,
        "gender_list": gender_list,
        "sex_list": sex_list,
        
>>>>>>> 0dd0e8873978aabfcddc5b40533c58533684585f
    }
    
    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def export_beneficiary_data(request):
    """
    This view handles the request for exporting Beneficiary data. The task is
    call to generate a export file, the task returns an ID which is used by
    the client to poll the status of the task.
    """
    task = generate_export_file.delay()

    # returns the task_id with the response
    response = {"task_id": task.task_id}
    return JsonResponse(response)


@login_required(login_url="/login/")
def poll_async_resullt(request, task_id):
    """
    This view handles the polling of state of the task the generates
    the export file. If the task is finnished, the appropriate response
    returned, which includes the download url for the file.
    """
    task = AsyncResult(task_id)

    media_url = settings.MEDIA_URL

    if task.state == "SUCCESS":
        download_url = f"{media_url}exports/{task.result}"
        body = {"state": task.state, "location": download_url}
        return JsonResponse(body, status=201)

    elif task.state == "PENDING":
        body = {"state": task.state}
        return JsonResponse(body, status=200)
    else:
        return JsonResponse({"error": f"No task with id {task_id}"}, status=400)


@login_required(login_url="/login/")
def uielements(request):
    context = {"title": "UI Elements"}
    html_template = loader.get_template("home/basic_elements.html")
    return HttpResponse(html_template.render(context, request))


class MedicalRecordListView(LoginRequiredMixin, ListView):
    template_name = "beneficiary/medical_record_list.html"
    model = MedicalRecord

    def get_queryset(self):
        return MedicalRecord.objects.filter(beneficiary=self.kwargs["beneficiary_id"])

    def get_context_data(self, **kwargs):
        # Benenficiary-098123hjkf/medical_record_list
        context = super(MedicalRecordListView, self).get_context_data(**kwargs)
        context["beneficiary"] = Beneficiary.objects.get(
            pk=self.kwargs["beneficiary_id"]
        )
        context["title"] = "Medical Records"
        return context


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    """
    Display details of a single beneficiary medical record.
    """

    context_object_name = "medical_record"
    template_name = "beneficiary/medical_record_detail.html"
    model = MedicalRecord

    def get_context_data(self, **kwargs):
        context = super(MedicalRecordDetailView, self).get_context_data(**kwargs)
        context["title"] = "Medical Record"
        return context


class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new MedicalRecord
    """

    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = "beneficiary/medical_record_create.html"

    def get_success_url(self): 
        return reverse("beneficiary:details", kwargs={"pk": self.object.beneficiary.pk})

    def get_context_data(self, **kwargs):
        context = super(MedicalRecordCreateView, self).get_context_data(**kwargs)
        context["title"] = "add medical record"
        return context

    def form_valid(self, form):
        beneficiary_object_id = self.kwargs.get('beneficiary_id', None)
        form.instance.beneficiary = Beneficiary.objects.get(id=beneficiary_object_id)
        return super(MedicalRecordCreateView, self).form_valid(form)

<<<<<<< HEAD


        


=======
>>>>>>> 0dd0e8873978aabfcddc5b40533c58533684585f
class BeneficiaryCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Beneficiary object.
    """

    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = "beneficiary/beneficiary_create.html"

    def get_success_url(self):
        return reverse("beneficiary:details")

    def get_context_data(self, **kwargs):
        context = super(BeneficiaryCreateView, self).get_context_data(**kwargs)
        context["title"] = "create new beneficiary"
        return context


class BenenficiaryListView(LoginRequiredMixin, ListView):
    """
    Beneficiary  List View.
    """

    context_object_name = "beneficiaries"
    model = Beneficiary
    paginate_by = 10
    template_name = "beneficiary/beneficiary_list.html"

    def get_queryset(self):

        if "q" in self.request.GET:
            q = self.request.GET["q"]
            beneficiary = Beneficiary.objects.filter(
                alive=True and
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(beneficiary_id__icontains=q)
            )

        else:
            beneficiary = Beneficiary.objects.filter(alive=True)
        return beneficiary

    def get_context_data(self, **kwargs):
        beneficiary_resource = BeneficiaryResource()
        export_data = beneficiary_resource.export()
        export_type = export_data.json

        context = super(BenenficiaryListView, self).get_context_data(**kwargs)
        context["opd"] = Service.objects.filter(client_type="OPD").count()
        context["hts"] = Service.objects.filter(service_type="HTS").count()
        context["vl"] = Service.objects.filter(service_type="VL").count()
        context["art"] = Service.objects.filter(client_type="ART").count()
        context["labs"] = Service.objects.filter(service_type="LAB").count()
        context["pharmacy"] = Service.objects.filter(service_type="PHARMACY").count()
        context["registered_today"] = Beneficiary.total_registered_today()
        context["title"] = "Beneficiaries"

        return context


class AgentCreateView(LoginRequiredMixin, CreateView):
    """
      Create an agent object.
    """

    model = Agent
    form_class = AgentForm
    template_name = "agent/agent_create.html"

    def get_success_url(self):
        return reverse("beneficiary:agent_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AgentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AgentCreateView, self).get_context_data(**kwargs)
        roles = RolesManager.get_roles_names()

        context["title"] = "create agent"
        context["roles"] = roles

        return context


class AgentListView(LoginRequiredMixin, ListView):
    """
    List all agent users.
    """

    model = Agent
    context_object_name = "agents"
    template_name = "agent/agent_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AgentListView, self).get_context_data(**kwargs)
        context["title"] = "list all agents"
        return context


class AgentDetailView(LoginRequiredMixin, DetailView):
    """
    Agent Details view.
    """

    context_object_name = "agent"
    model = Agent
    template_name = "agent/agent_detail.html"

    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data(**kwargs)
        context["title"] = "Agent User Details"

        return context


class BeneficiaryDetailView(LoginRequiredMixin, DetailView):
    """
    Beneficiary Details view.
    """

    context_object_name = "beneficiary"
    model = Beneficiary
    template_name = "beneficiary/beneficiary_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BeneficiaryDetailView, self).get_context_data(**kwargs)
        current_beneficiary_id = self.kwargs.get('pk')
        current_beneficiary = Beneficiary.objects.get(id=current_beneficiary_id) 
        beneficiary_medical_records = MedicalRecord.objects.filter(beneficiary__id=current_beneficiary_id)
        
        services = { 
           "services": [] 
        }

        medications = { 
            "medications": []
        }

        labs = []

        # Get all services for the beneficiary
        for medical_record in beneficiary_medical_records:            
            service_personnel_name = medical_record.service.service_personnel.first_name + " " + medical_record.service.service_personnel.last_name
            
            services["services"].append(
                {
                    "service_object": medical_record.service,
                    "service_facility": medical_record.service_facility,
                    "service_provider" : service_personnel_name,
                    "service_comments" : medical_record.provider_comments,
                }
            )            
        # Get all labs for beneficiary
        for lab in beneficiary_medical_records:
            lab_entry = lab.lab
            labs.append(lab_entry)

        # Get all prescriptions for beneficiary
        for medication in beneficiary_medical_records:
            medications["medications"].append(
                {
                    "prescription_title": medication.prescription.title,
                    "drugs_to_take": medication.prescription.drugs.name,
                    "when_to_take": medication.when_to_take,
                    "no_of_days": medication.no_of_days,
                    "date_prescribed": medication.prescription.date 
                }

            ) 
                   
        # Table Paginators
        medication_paginator_list = []
        for _, values in medications.items():
            for medication in values:
                medication_paginator_list.append(medication["prescription_title"])

        services_paginator_list = []
        for _, values in services.items():
            for service in values:
                services_paginator_list.append(service["service_object"])


        medication_paginator = Paginator(medication_paginator_list, 2)
        page = self.request.GET.get('medical_page')
        medication_paginator_list = medication_paginator.get_page(page)
        
        service_paginator = Paginator(services_paginator_list, 2)
        service_page = self.request.GET.get('service_page')
        service_paginator_list = service_paginator.get_page(service_page)
        
        labs_paginator = Paginator(labs, 2)
        lab_page = self.request.GET.get('labs_page')
        labs = labs_paginator.get_page(lab_page)
        
        context["title"] = "Beneficiary Details"
        context["service_title"] = "services"
        context["medication_title"] = "medications"
        context["lab_title"] = "labs"
        context["beneficiary"] = current_beneficiary
        context['services']  = services
        context['service_paginator_list']  = service_paginator_list
        context['labs']  = labs        
        context['medications'] = medications
        context['medication_paginator_list'] = medication_paginator_list
        return context


@login_required(login_url="/login/")
def user_events(request):
    users = User.objects.all()
    # users_list = [user for user in users]
    page_num = request.GET.get("page", 1)
    p = Paginator(users, 2)

    page_obj = p.get_page(page_num)
    context = {"users_list": page_obj}

    html_template = loader.get_template("home/events.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def beneficiary_report(request):
    # Graphs
    # Number of beneficiaries by year
    year1 = Beneficiary.objects.filter(created__year=2017).values("created__year").count()
    year2 = Beneficiary.objects.filter(created__year=2018).values("created__year").count()
    year3 = Beneficiary.objects.filter(created__year=2019).values("created__year").count()
    year4 = Beneficiary.objects.filter(created__year=2020).values("created__year").count()
    year5 = Beneficiary.objects.filter(created__year=2021).values("created__year").count()

    # Number of beneficiaries by province
    count_records = {}
    count_services={}
    province_labels = []
    beneficiary_count_data = []

    for province in Province.objects.all():
        total_province_beneficiaries = Beneficiary.objects.filter(registered_facility__province__name=province.name).count()
        total_province_services = MedicalRecord.objects.filter(service_facility__province__name=province.name).count()

        province_data = {
            province.name: total_province_beneficiaries
        }

        service_data = {
            province.name: total_province_services
        }

        count_records.update(province_data)
        count_services.update(service_data)

        province_labels.append(province.name)
        beneficiary_count_data.append(total_province_beneficiaries)

        province_label_json_list = json.dumps(province_labels);
    
    # Service Counts by Month
     
           

    # Number of total interactions
    total_interactions = MedicalRecord.objects.all().count()
    
    
    # Dashboar Cards Stats
    opd = Service.objects.filter(client_type="OPD").count()
    hts = Service.objects.filter(service_type="HTS").count()
    vl = Service.objects.filter(service_type="VL").count()
    art = Service.objects.filter(client_type="ART").count()
    labs = Service.objects.filter(service_type="LAB").count()
    pharmacy = Service.objects.filter(service_type="PHARMACY").count()
    male = Beneficiary.objects.filter(gender='Male').count()
    female = Beneficiary.objects.filter(gender='Female').count()
    transgender = Beneficiary.objects.filter(gender='Transgender').count()
    other = Beneficiary.objects.filter(gender='Other').count()
    male_sex = Beneficiary.objects.filter(sex='Male').count()
    female_sex = Beneficiary.objects.filter(sex='Female').count()

    context = {
        "data": [],
        "opd": opd,
        "hts": hts,
        "vl": vl,
        "art": art,
        "labs": labs,
        "pharmacy": pharmacy,
        "male": male,
        "female": female,
        "transgender": transgender, 
        "other": other,
        "male_sex": male_sex, 
        "female_sex": female_sex,
        "year1" : year1,
        "year2" : year2,
        "year3" : year3,
        "year4" : year4,
        "year5" : year5,
        "total_interactions" : total_interactions,
        "province_label_json_list" : province_label_json_list,
        "beneficiary_count_data" : beneficiary_count_data
        
    }

    html_template = loader.get_template("home/reports.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


def doughnutChart(request):
    femaleSex = Beneficiary.objects.filter(sex="Female")
    maleSex = Beneficiary.objects.filter(sex="Male")
