import django_filters

from .models import Beneficiary


class BeneficiaryFilter(django_filters.FilterSet):
    class Meta:
        model = Beneficiary
        fields = ["first_name", "last_name", "agent_id", "gender", "beneficiary_id"]
