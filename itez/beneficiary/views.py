# -*- encoding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django.views.generic import TemplateView

from itez.beneficiary.models import Beneficiary


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


class BeneficiaryListView(LoginRequiredMixin, ListView):
    model = Beneficiary
    template_name = 'home/list_beneficiary.html'
    context_object_name = 'beneficiaries'
    paginate_by = settings.ITEMS_PER_PAGE

    def get_queryset(self):
        return Beneficiary.objects.all()


@login_required(login_url="/login/")
def user_events(request):

    context = {"events": []}

    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def beneficiary_report(request):

    context = {"data": []}

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
