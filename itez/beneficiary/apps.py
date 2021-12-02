from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BeneficiaryConfig(AppConfig):
    name = "itez.beneficiary"
    verbose_name = _("Beneficiary")

    def ready(self):
        from itez.beneficiary import signals