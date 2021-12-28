from django.contrib.gis import forms

from django.forms import ModelForm, widgets
from django.contrib.gis.geos import Point

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    HTML,
    Submit,
    Row,
    Column,
    Field,
    Div,
    MultiField,
)
from crispy_forms.bootstrap import FormActions
from crispy_forms.bootstrap import TabHolder, Tab
from mapwidgets.widgets import GooglePointFieldWidget

from itez.beneficiary.models import Beneficiary, MedicalRecord
from itez.beneficiary.models import Agent


class MedicalRecordForm(ModelForm):
    documents = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

    class Meta:

        model = MedicalRecord
        exclude = ["created", "medical_record_id", "beneficiary"]
        widgets = {
            'interaction_date': widgets.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'type':'date'}),
            'provider_comments': forms.TextInput(attrs={'size': 500, 'title': 'Extra notes or comments',  'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Service",
                Row(
                    Column("service_facility", css_class="form-group col-md-6 mb-0"),
                    Column("interaction_date", css_class="form-group col-md-6 mb-0"),
                    Column("service", css_class="form-group col-md-6 mb-0"),
                    Column("documents", css_class="form-group col-md-6 mb-0"),
                    Column("provider_comments", css_class="form-group col-md-12 mb-0"),
                    Column("prescription", css_class="form-group col-md-12 mb-0"),
                    Column("when_to_take", css_class="form-group col-md-12 mb-0"),
                    Column("no_of_days", css_class="form-group col-md-12 mb-0"),
                    Column("lab", css_class="form-group col-md-12 mb-0"),
                    Column("approved_by", css_class="form-group col-md-12 mb-0"),
                    Column("approver_signature", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
            ),
            FormActions(
                Submit("save", "Create Medical Record"),
                HTML('<a class="btn btn-danger" href="/beneficiary/list">Cancel</a>'),
            ),
        )

    def save(self, commit=True):
        instance = super(MedicalRecordForm, self).save(commit=False)
        instance.save()
        self.save_m2m()
        return instance


class AgentForm(ModelForm):
    class Meta:

        model = Agent
        exclude = ["created", "agent_id"]
        widgets = {
            "birthdate": widgets.DateInput(attrs={"type": "date"}),
            "location": GooglePointFieldWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Personal Details",
                Row(
                    Div("user", css_class="form-group col-md-6 mb-0"),
                    Div("first_name", css_class="form-group col-md-6 mb-0"),
                    Div("last_name", css_class="form-group col-md-6 mb-0"),
                    Div("birthdate", css_class="form-group col-md-6 mb-0"),
                    Div("gender", css_class="form-group col-md-6 mb-0"),
                ),
            ),
            Fieldset(
                "Other Meta Data",
                Row(
                    Div("location", css_class="form-group col-md-12 mb-0"),
                    css_class="form-row",
                ),
            ),
            FormActions(
                Submit("submit", "Create Agent"),
                HTML('<a class="btn btn-danger" href="/agent/list">Cancel</a>'),
            ),
        )

    def save(self, commit=True):
        instance = super(AgentForm, self).save(commit=False)
        if commit:
            instance.save()
        # self.save_m2m()  # we  can use this if we have many to many field on the model i.e Service
        return instance


class BeneficiaryForm(ModelForm):
    class Meta:

        model = Beneficiary
        exclude = ["created", "beneficiary_id"]
        widgets = {
            "date_of_birth": widgets.DateInput(
                format=("%m/%d/%Y"), attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Personal Information",
                Row(
                    Column("first_name", css_class="form-group col-md-6 mb-0"),
                    Column("last_name", css_class="form-group col-md-6 mb-0"),
                    Column("other_name", css_class="form-group col-md-6 mb-0"),
                    Column("gender", css_class="form-group col-md-6 mb-0"),
                    Column("sex", css_class="form-group col-md-6 mb-0"),
                    Column("profile_photo", css_class="form-group col-md-6 mb-0"),
                    Column("phone_number", css_class="form-group col-md-6 mb-0"),
                    Column("email", css_class="form-group col-md-6 mb-0"),
                    Column("date_of_birth", css_class="form-group col-md-6 mb-0"),
                    Column("marital_status", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Family Information",
                Row(
                    Column("name_of_spouse", css_class="form-group col-md-4 mb-0"),
                    Column("number_of_children", css_class="form-group col-md-4 mb-0"),
                    Column("number_of_siblings", css_class="form-group col-md-4 mb-0"),
                    Column("parent_details", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Other Meta Data",
                Row(
                    Column("registered_facility", css_class="form-group col-md-4 mb-0"),
                    Column("alive", css_class="form-group col-md-4 mb-0"),
                    Column("education_level", css_class="form-group col-md-4 mb-0"),
                    Column("hiv_status", css_class="form-group col-md-4 mb-0"),
                    Column("art_status", css_class="form-group col-md-4 mb-0"),
                    Column("last_vl", css_class="form-group col-md-4 mb-0"),
                    Column("alive", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
            ),
            FormActions(
                Submit("save", "Create Beneficiary"),
                HTML('<a class="btn btn-danger" href="/beneficiary/list">Cancel</a>'),
            ),
        )
        super(BeneficiaryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BeneficiaryForm, self).save(commit=False)
        if commit:
            instance.save()
        # self.save_m2m()  # we  can use this if we have many to many field on the model i.e Service
        return instance
