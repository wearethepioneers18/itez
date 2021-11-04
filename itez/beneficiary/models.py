from django.db import models
from django.db.models.deletion import PROTECT 
from django.utils.translation import gettext_lazy as _



class Province(models.Model):
    """
    Implements province properties and required methods.
    """
    name = models.CharField(
        _("Province"),
        max_length=255 
    )

    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'
        ordering = ['-created']
    

class District(models.Model):
    """
    Define district properties and corresponding methods.
    """
    
    name = models.CharField(
        _('District'),
        max_length=255
    )

    province = models.ForeignKey(
        Province,
        on_delete=PROTECT,
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    """
    Define service area properties.
    """
    name = models.CharField(
        _('Service Area'),
        max_length=200
    )

    district = models.ForeignKey(
        District,
        on_delete=PROTECT
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkDetail(models.Model):
    """
    Include Work Detail properties. 
    """
    gross_pay = models.DecimalField( 
        _("Monthly Salary"),
        decimal_places=2,
        max_digits=1000,
        null=False
    )
    company = models.CharField(
        _("Company Name"),
        max_length=200,
        null=False
    )
    insured = models.BooleanField(
        _("Company Insured"),
        default = False
    )
    work_address = models.TextField(
        _("Work Address"),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.company
