from django.contrib.auth import forms

from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column
from itez.beneficiary.models import BeneficiaryService


class MedicalRecordForm(ModelForm):   


    class Meta:

        model = BeneficiaryService
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
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-danger'))
