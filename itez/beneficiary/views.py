# -*- encoding: utf-8 -*-
import json
import datetime
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
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from itez.beneficiary.forms import BeneficiaryForm
from itez.beneficiary.models import (
    GENDER_CHOICES, 
    SEX_CHOICES, 
    EDUCATION_LEVEL,
    HIV_STATUS_CHOICES,
    MARITAL_STATUS,
    ART_STATUS_CHOICES,
)
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
    District,
    Facility,
    MedicalRecord,
    Province,
    Agent,
    Service,
)

from django.core.paginator import Paginator
from .tasks import generate_export_file

from itez.beneficiary.forms import BeneficiaryForm, MedicalRecordForm, AgentForm
from itez.users.models import User

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
        "sunday": sun_day,
        "monday": mon_day,
        "tuesday": tue_day,
        "wednesday": wed_day,
        "thursday": thu_day,
        "friday": fri_day,
        "saturday": sat_day,
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
    html_template = loader.get_template("beneficiary/test_details.html")
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
  

class BeneficiaryDetailView(LoginRequiredMixin, DetailView):
	"""
	Beneficiary Details view.
	"""

	context_object_name = "beneficiary"
	model = Beneficiary
	paginate_by = 2
	template_name = "beneficiary/beneficiary_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(BeneficiaryDetailView, self).get_context_data(**kwargs)
		current_beneficiary_id = self.kwargs.get('pk')
		current_beneficiary = Beneficiary.objects.get(id=current_beneficiary_id) 
		beneficiary_medical_records = MedicalRecord.objects.filter(beneficiary__id=current_beneficiary_id)
		latest_beneficiary_medical_record = MedicalRecord.objects.filter(beneficiary__id=current_beneficiary_id).latest('created')
		print("Service Provider" + str(latest_beneficiary_medical_record.service.document))
		
		services = { 
		   "services": [] 
		}  


		service_provider_name = latest_beneficiary_medical_record.service.service_personnel.first_name + "" + latest_beneficiary_medical_record.service.service_personnel.last_name
		latest_beneficiary_service = {

			"service_name": latest_beneficiary_medical_record.service,
			"service_facility":  latest_beneficiary_medical_record.service_facility,
			"interaction_date": latest_beneficiary_medical_record.interaction_date,
			"service_provider": service_provider_name,
			"service_provider_comments": latest_beneficiary_medical_record.provider_comments,
			"supporting_documents": latest_beneficiary_medical_record.document,
			"prescription": latest_beneficiary_medical_record.prescription.title,
			"when_to_take" : latest_beneficiary_medical_record.when_to_take
		}      

		# Get all services for the beneficiary
		for medical_record in beneficiary_medical_records:            
			service_personnel_name = medical_record.service.service_personnel.first_name + "  " + medical_record.service.service_personnel.last_name
			
			services["services"].append(
				{
					"service_object": medical_record.service,
					"service_facility": medical_record.service_facility,
					"service_provider" : service_personnel_name,
					"service_comments" : medical_record.provider_comments,
				}
			)      
		
		services_paginator_list = []
		for _, values in services.items():
			for service in values:
				services_paginator_list.append(service["service_object"])


		service_paginator = Paginator(services["services"], 5)
		service_page_number = self.request.GET.get('service_page')
		service_paginator_list = service_paginator.get_page(service_page_number)

		medical_record_latest = MedicalRecord.objects.latest('created')

						
		context["title"] = "Beneficiary Details"
		context["service_title"] = "services"
		context["medication_title"] = "medications"
		context["lab_title"] = "labs"
		context["beneficiary"] = current_beneficiary
		context['service_paginator_list']  = service_paginator_list
		context['latest_beneficiary_service'] = latest_beneficiary_service
		return context


      
class BeneficiaryCreateView(LoginRequiredMixin, CreateView):
	"""
	Create a new Beneficiary object.
	"""

	model = Beneficiary
	form_class = BeneficiaryForm
	template_name = "beneficiary/beneficiary_create.html"

	def get_success_url(self):
		return reverse("beneficiary:list")

	def get_context_data(self, **kwargs):
		context = super(BeneficiaryCreateView, self).get_context_data(**kwargs)
		context["title"] = "create new beneficiary"
		return context


class BeneficiaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Beneficiary
    template_name = "beneficiary/beneficiary_update.html"
    success_url = "/beneficiary/list"
    form_class = BeneficiaryForm
    
    def get_context_data(self, **kwargs):
        context = super(BeneficiaryUpdateView, self).get_context_data(**kwargs)
        beneficiary_id = self.kwargs.get("pk")  
        beneficiary = Beneficiary.objects.get(id=beneficiary_id)
        form = BeneficiaryForm(instance=beneficiary)
        context["title"] = "update beneficiary"
        context["form"] = form
        return context

class AgentUpdateView(LoginRequiredMixin, UpdateView):
    model = Agent
    template_name = "agent/agent_update.html"
    success_url = "/agent/list"
    # form_class = AgentForm
    fields = [
        'first_name',
        'last_name',
        'location',
        'birthdate',
        'gender'
    ]
    
    def get_context_data(self, **kwargs):
        context = super(AgentUpdateView, self).get_context_data(**kwargs)
        agent_id = self.kwargs.get("pk")  
        agent = Agent.objects.get(id=agent_id)
        form = AgentForm(instance=agent)
        if form.is_valid():
            form.save()
        context["title"] = "update agent"
        context["form"] = form
        return context


@login_required(login_url="/login/")
def beneficiary_delete_view(request, pk):
    beneficiary = Beneficiary.objects.get(id=pk)
    beneficiary.delete()
    return redirect(reverse("beneficiary:list"))

@login_required(login_url="/login/")
def agent_delete_view(request, pk):
    agent = Agent.objects.get(id=pk)
    agent.delete()
    return redirect(reverse("beneficiary:agent_list"))
  
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
                alive=True
                and Q(first_name__icontains=q)
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


class BeneficiaryDetailView(LoginRequiredMixin, DetailView):
    """
    Beneficiary Details view.
    """

    context_object_name = "beneficiary"
    model = Beneficiary
    paginate_by = 2
    template_name = "beneficiary/beneficiary_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BeneficiaryDetailView, self).get_context_data(**kwargs)
        current_beneficiary_id = self.kwargs.get("pk")
        current_beneficiary = Beneficiary.objects.get(id=current_beneficiary_id)
        beneficiary_medical_records = MedicalRecord.objects.filter(
            beneficiary__id=current_beneficiary_id
        )
        latest_beneficiary_medical_record = MedicalRecord.objects.filter(
            beneficiary__id=current_beneficiary_id
        ).latest("created")
        print(
            "Service Provider" + str(latest_beneficiary_medical_record.service.document)
        )

        services = {"services": []}

        service_provider_name = (
            latest_beneficiary_medical_record.service.service_personnel.first_name
            + ""
            + latest_beneficiary_medical_record.service.service_personnel.last_name
        )
        latest_beneficiary_service = {
            "service_name": latest_beneficiary_medical_record.service,
            "service_facility": latest_beneficiary_medical_record.service_facility,
            "interaction_date": latest_beneficiary_medical_record.interaction_date,
            "service_provider": service_provider_name,
            "service_provider_comments": latest_beneficiary_medical_record.provider_comments,
            "supporting_documents": latest_beneficiary_medical_record.document,
            "prescription": latest_beneficiary_medical_record.prescription.title,
            "when_to_take": latest_beneficiary_medical_record.when_to_take,
        }

        # Get all services for the beneficiary
        for medical_record in beneficiary_medical_records:
            service_personnel_name = (
                medical_record.service.service_personnel.first_name
                + "  "
                + medical_record.service.service_personnel.last_name
            )

            services["services"].append(
                {
                    "service_object": medical_record.service,
                    "service_facility": medical_record.service_facility,
                    "service_provider": service_personnel_name,
                    "service_comments": medical_record.provider_comments,
                }
            )

        services_paginator_list = []
        for _, values in services.items():
            for service in values:
                services_paginator_list.append(service["service_object"])

        service_paginator = Paginator(services["services"], 2)
        service_page_number = self.request.GET.get("service_page")
        service_paginator_list = service_paginator.get_page(service_page_number)

        medical_record_latest = MedicalRecord.objects.latest("created")

        context["title"] = "Beneficiary Details"
        context["service_title"] = "services"
        context["medication_title"] = "medications"
        context["lab_title"] = "labs"
        context["beneficiary"] = current_beneficiary
        context["service_paginator_list"] = service_paginator_list
        context["latest_beneficiary_service"] = latest_beneficiary_service
        return context


class BeneficiaryCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Beneficiary object.
    """

    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = "beneficiary/beneficiary_create.html"

    def get_success_url(self):
        return reverse("beneficiary:list")

    def get_context_data(self, **kwargs):
        context = super(BeneficiaryCreateView, self).get_context_data(**kwargs)
        context["title"] = "create new beneficiary"
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
    
    current_year = datetime.datetime.now().year
    year_one = current_year - 1
    year_two = current_year - 2
    year_three = current_year - 3
    year_four = current_year - 4
    
    year1 = (
        Beneficiary.objects.filter(created__year=year_four).values("created__year").count()
    )
    year2 = (
        Beneficiary.objects.filter(created__year=year_three).values("created__year").count()
    )
    year3 = (
        Beneficiary.objects.filter(created__year=year_two).values("created__year").count()
    )
    year4 = (
        Beneficiary.objects.filter(created__year=year_one).values("created__year").count()
    )
    year5 = (
        Beneficiary.objects.filter(created__year=current_year).values("created__year").count()
    )

    # Number of beneficiaries by province
    count_records = {}
    count_services = {}
    province_labels = []
    beneficiary_count_data = []

    for province in Province.objects.all():
        total_province_beneficiaries = Beneficiary.objects.filter(
            registered_facility__province__name=province.name
        ).count()
        total_province_services = MedicalRecord.objects.filter(
            service_facility__province__name=province.name
        ).count()

        province_data = {province.name: total_province_beneficiaries}

        service_data = {province.name: total_province_services}

        count_records.update(province_data)
        count_services.update(service_data)

        province_labels.append(province.name)
        beneficiary_count_data.append(total_province_beneficiaries)

        province_label_json_list = json.dumps(province_labels)

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
    male = Beneficiary.objects.filter(gender="Male").count()
    female = Beneficiary.objects.filter(gender="Female").count()
    transgender = Beneficiary.objects.filter(gender="Transgender").count()
    other = Beneficiary.objects.filter(gender="Other").count()
    male_sex = Beneficiary.objects.filter(sex="Male").count()
    female_sex = Beneficiary.objects.filter(sex="Female").count()

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
        "year1": year1,
        "year2": year2,
        "year3": year3,
        "year4": year4,
        "year5": year5,
        "total_interactions": total_interactions,
        "province_label_json_list": province_label_json_list,
        "beneficiary_count_data": beneficiary_count_data,
    }

    html_template = loader.get_template("home/reports.html")
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
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
