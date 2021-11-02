from django.db import models
from django.utils.translation import gettext_lazy as _

class Province(models.Model):
    """
    Implements province properties and required methods.
    """
    name = models.CharField(
        _("Province"),
        max_length=255, 
        null=True, 
        blank=True
        )

    created = models.DateTimeField(auto_now_add=True)

    
