from django.contrib.auth import forms

from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Submit, Row, Column
from crispy_forms.bootstrap import FormActions
from itez.beneficiary.models import Beneficiary, MedicalRecord


class MedicalRecordForm(ModelForm):   


    class Meta:

        model = MedicalRecord
        exclude = ['created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        # self.helper.layout = Layout(
        #     Fieldset(
        #         'Medical Record',
        #         Row(
        #             Column('name', css_class='form-group col-md-6 mb-0'),
        #             Column('age', css_class='form-group col-md-6 mb-0'),
        #             css_class='form-row'
        #         ),
        #         Row(
        #             Column('
        #         ),
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(
            'submit', 
            'Create Medica Record'
            )
        )
        self.helper.add_input(Submit(
            'cancel', 
            'Cancel', 
            css_class='btn-danger', formnovalidate='formnovalidate'))


class BeneficiaryForm(ModelForm):   


    class Meta:

        model = Beneficiary
        exclude = ['created', 'beneficiary_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Personal Details",
                'first_name',
                'last_name',
                'phone_number',
                'email',
                'gender',
                'sex',
                'date_of_birth',
                'address',
            ),
            Fieldset(
                'Family Details',
                'marital_status',
                'name_of_spouse',
                'number_of_children',
                'number_of_siblings',
                'parent_details',
            ),
            Fieldset(
                'Meta Data',
                'agent',
                'education_level',
                'alive',
            ),
            FormActions(
                Submit('save', 'Create Beneficiary'),
                HTML('<a class="btn btn-danger" href="/beneficiary/list">Cancel</a>'),
            )
        )
       
