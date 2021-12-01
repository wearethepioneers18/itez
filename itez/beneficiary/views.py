# -*- encoding: utf-8 -*-

from django import template
from django.contrib.gis.db.models import fields
from django.views.generic import CreateView, FormView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.list import ListView

from itez.beneficiary.models import Beneficiary, BeneficiaryParent, BeneficiaryService
from itez.beneficiary.models import Service

from itez.beneficiary.forms import MedicalRecordForm


@login_required(login_url="/login/")
def index(request):
    opd = Service.objects.filter(client_type='OPD').count()
    hts = Service.objects.filter(service_type='HTS').count()
    vl = Service.objects.filter(service_type='VL').count()
    art = Service.objects.filter(client_type='ART').count()    
    labs = Service.objects.filter(service_type='LAB').count()
    pharmacy = Service.objects.filter(service_type='PHARMACY').count()
    male = Beneficiary.objects.filter(gender = 'Male').count()
    female = Beneficiary.objects.filter(gender = 'Female').count()
    transgender = Beneficiary.objects.filter(gender = 'Transgender').count
    other = Beneficiary.objects.filter(gender = 'Other').count()
   
    context = {'segment': 'index', "opd": opd, "hts": hts, "vl": vl, "art": art, "lab": labs, "pharmacy": pharmacy, "male": male, "female": female, "transgender": transgender, "other": other}
    

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def uielements(request):    
    context = {'title': 'UI Elements'}
    html_template = loader.get_template('home/basic_elements.html')
    return HttpResponse(html_template.render(context, request))


class FormActionMixin(object):
    """
    Add 'cancel' button redirect to medical record list.
    """
    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            medical_record_list_url = reverse('medical_record_list')
            return HttpResponseRedirect(medical_record_list_url)

        else:
            return super(FormActionMixin, self).post(request, *args, **kwargs)


class MedicalRecordListView(ListView):
    template_name = 'beneficiary/medical_record_list.html'
    model = BeneficiaryService

    def  get_queryset(self):
        return BeneficiaryService.objects.filter(beneficiary=self.kwargs['beneficiary_id'])

    def get_context_data(self, **kwargs):
        # Benenficiary-098123hjkf/medical_record_list
        context = super(MedicalRecordListView, self).get_context_data(**kwargs)
        context['beneficiary'] = Beneficiary.objects.get(pk=self.kwargs['beneficiary_id'])
        context['title'] = 'Medical Records'
        return context

class  MedicalRecordCreateView(FormActionMixin, CreateView):
    """
    Create a new MedicalRecord
    """
    model = BeneficiaryService
    form_class = MedicalRecordForm
    template_name = 'beneficiary/medical_record_create.html'

    def get_success_url(self):
        return reverse('beneficiary:medical_record_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MedicalRecordCreateView, self).form_valid(form)
    
    
    


@login_required(login_url="/login/")
def list_beneficiary(request):
    beneficiaries = Beneficiary.objects.all()
    beneficiary_list = [beneficiary for beneficiary in beneficiaries]
    opd = Service.objects.filter(client_type='OPD').count()
    hts = Service.objects.filter(service_type='HTS').count()
    vl = Service.objects.filter(service_type='VL').count()
    art = Service.objects.filter(client_type='ART').count()    
    labs = Service.objects.filter(service_type='LAB').count()
    pharmacy = Service.objects.filter(service_type='PHARMACY').count()
    

    

    context = {"beneficiaries": beneficiary_list, "opd": opd, "hts": hts, "vl": vl, "art": art, "lab": labs, "pharmacy": pharmacy}

    html_template = loader.get_template('beneficiary/list_beneficiary.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def user_events(request):
    opd = Service.objects.filter(client_type='OPD').count()
    hts = Service.objects.filter(service_type='HTS').count()
    vl = Service.objects.filter(service_type='VL').count()
    art = Service.objects.filter(client_type='ART').count()    
    labs = Service.objects.filter(service_type='LAB').count()
    pharmacy = Service.objects.filter(service_type='PHARMACY').count()

    context = {"events": [], "opd": opd, "hts": hts, "vl": vl, "art": art, "lab": labs, "pharmacy": pharmacy}

    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def beneficiary_report(request):
    opd = Service.objects.filter(client_type='OPD').count()
    hts = Service.objects.filter(service_type='HTS').count()
    vl = Service.objects.filter(service_type='VL').count()
    art = Service.objects.filter(client_type='ART').count()    
    labs = Service.objects.filter(service_type='LAB').count()
    pharmacy = Service.objects.filter(service_type='PHARMACY').count()

    context = {"data": [], "opd": opd, "hts": hts, "vl": vl, "art": art, "lab": labs, "pharmacy": pharmacy}

    html_template = loader.get_template('home/reports.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def doughnutChart(request):
    femaleSex = Beneficiary.objects.filter(sex = 'Female')
    maleSex = Beneficiary.objects.filter(sex = 'Male')


    




