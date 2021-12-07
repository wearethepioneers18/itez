from django.contrib.auth import forms

from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Submit, Row, Column, Field, Div
from crispy_forms.bootstrap import FormActions
from crispy_forms.bootstrap import TabHolder, Tab

from itez.beneficiary.models import Beneficiary, MedicalRecord


class MedicalRecordForm(ModelForm):
    class Meta:

        model = MedicalRecord
        exclude = ["created"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                "Service",
                Row(
                    Column("beneficiary", css_class="form-group col-md-6 mb-0"),
                    Column("service", css_class="form-group col-md-6 mb-0"),
                    Column("provider_comments", css_class="form-group col-md-6 mb-0"),
                    Column("interaction_date", css_class="form-group col-md-6 mb-0"),
                    Column("service_facility", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Medication",
                Row(
                    Column("prescription", css_class="form-group col-md-4 mb-0"),
                    Column("no_of_days", css_class="form-group col-md-4 mb-0"),
                    Column("when_to_take", css_class="form-group col-md-4 mb-0"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Lab",
                Row(
                    Column("lab", css_class="form-group col-md-12  mb-0"),
                    css_class="form-row",
                ),
            ),
            FormActions(
                Submit("save", "Create Medica Record"),
                HTML('<a class="btn btn-danger" href="/beneficiary/list">Cancel</a>'),
            ),
        )

    def save(self, commit=True):
        instance = super(BeneficiaryForm, self).save(commit=False)
        instance.save()
        self.save_m2m()
        return instance


class BeneficiaryForm(ModelForm):
    class Meta:

        model = Beneficiary
        exclude = ["created", "beneficiary_id"]

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
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
