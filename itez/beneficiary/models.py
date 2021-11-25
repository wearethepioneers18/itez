from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


GENDER_CHOICES = (
    ("Male", _("Male")),
    ("Female", _("Female")),
    ("Transgender", _("Transgender")),
    ("Other", _("Other"))
)
SEX_CHOICES = (
    ("Male", _("Male")),
    ("Female", _("Female"))
)


class AgentDetail(models.Model):
    """
    Create agent detail table with its attributes or columns.
    """

    first_name = models.CharField(
        _("First Name"),
        max_length=200,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        _("Second Name"),
        max_length=200,
        null=False
    )
    birthdate = models.DateField(
        _("Birth Date"),
        auto_now_add=False,
        null=True,
        blank=True
    )
    agent_id = models.CharField(
        max_length=100,
        editable=False
    )
    gender = models.CharField(
        _("Gender"),
        max_length=50,
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES[3][0]
    )
    location = models.PointField(
        _("Location"),
        geography=True,
        blank=True,
        null=True,
        srid=4326
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Beneficiary(models.Model):
    """
    Implements the Beneficiary properties and required methods.
    """
    MARITAL_STATUS = (
        ("single", _("Single")),
        ("married", _("Married")),
        ("seperated", _("Seperated")),
        ("divorced", _("Divorced")),
        ("widowed", _("Widowed")),
    )

    EDUCATION_LEVEL = (
        ("none", _("None")),
        ("primary", _("Primary")),
        ("basic", _("Basic")),
        ("secondary", _("Secondary O'Level")),
        ("certificate", _("Certificate")),
        ("diploma", _("Diploma")),
        ("degree", _("Degree")),
        ("masters", _("Masters")),
        ("doctrate", _("Doctrate")),
        ("phd", _("PHD")),
    )

    first_name = models.CharField(
        _("First Name"),
        max_length=200
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=200
    )
    other_name = models.CharField(
        _("Other Name"),
        max_length=200,
        null=True,
        blank=True
    )
    gender = models.CharField(
        _("Gender"),
        max_length=100,
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES[3][0]
    )
    sex = models.CharField(
        _("Sex"),
        max_length=100,
        choices=SEX_CHOICES
    )
    profile_photo = ProcessedImageField(
        upload_to='profile_photo',
        processors=[ResizeToFill(512, 512)],
        format='JPEG',
        options={'quality': 100},
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=20,
        null=True,
        blank=True
    )
    email = models.EmailField(
        _("Email"),
        max_length=200,
        null=True,
        blank=True
    )
    beneficiary_id = models.CharField(
        max_length=100,
        editable=False
    )
    agent = models.ForeignKey(
        AgentDetail,
        on_delete=models.PROTECT
    )
    date_of_birth = models.DateField(_("Date of Birth"))

    marital_status = models.CharField(
        _("Marital Status"),
        choices=MARITAL_STATUS,
        max_length=100
    )
    name_of_spouse = models.CharField(
        _("Phone Number"),
        max_length=200,
        null=True,
        blank=True
    )
    number_of_children = models.IntegerField(
        _("Number of children"),
        null=True,
        blank=True
    )
    number_of_siblings = models.IntegerField(
        _("Number of siblings"),
        null=True,
        blank=True
    )
    parent_details = models.ForeignKey(
        'BeneficiaryParent',
        on_delete=models.PROTECT
    )
    education_level = models.CharField(
        _("Education level"),
        max_length=300,
        null=True,
        blank=True,
        choices=EDUCATION_LEVEL
    )
    service_provider = models.ManyToManyField('ServiceProviderPersonel')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Beneficiary"
        verbose_name_plural = "Beneficiaries"
        ordering = ["created"]


class BeneficiaryParent(models.Model):
    father_first_name = models.CharField(
        _("Father First Name"),
        max_length=200
    )
    father_last_name = models.CharField(
        _("Father Last Name"),
        max_length=200
    )
    mother_first_name = models.CharField(
        _("Mother First Name"),
        max_length=200
    )
    mother_last_name = models.CharField(
        _("Mother Last Name"),
        max_length=200
    )
    address = models.TextField(
        max_length=300,
        null=True,
        blank=True
    )
    father_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    mother_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    father_date_of_birth = models.DateField(
        _("Father's date of birth"),
        null=True,
        blank=True
    )
    mother_date_of_birth = models.DateField(
        _("Mother's date of birth"),
        null=True,
        blank=True
    )
    father_village = models.CharField(
        _("Father's Village"),
        max_length=200,
        null=True,
        blank=True
    )
    mother_village = models.CharField(
        _("Mother's Village"),
        max_length=200,
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Beneficiary Parents are \
            Father: {self.father_first_name} {self.father_last_name}, \
            Mother: {self.mother_first_name} {self.mother_last_name}"


class Province(models.Model):
    """
    Implements province properties and required methods.
    """

    name = models.CharField(_("Province"), max_length=255)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        ordering = ["-created"]


class District(models.Model):
    """
    Define district properties and corresponding methods.
    """

    name = models.CharField(
        _("District"), 
        max_length=255
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    """
    Define service area properties.
    """

    name = models.CharField(
        _("Service Area"), 
        max_length=200
    )

    district = models.ForeignKey(
        District, 
        on_delete=models.PROTECT
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

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
        default=False
    )
    work_address = models.TextField(
        _("Work Address"),
        null=True,
        blank=True
    )
    beneficiary = models.OneToOneField(
        Beneficiary,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.company


NGO = 1
COMPANY = 2
GOVERNMENT = 3
OTHER = 4
IP_TYPES =  (
    (NGO, _('Non-Profit Organization')),
    (COMPANY, _('Company')),
    (GOVERNMENT, _('Government')),
    (OTHER, _('Other')),
)
class ImplementingPartner(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    ip_type = models.IntegerField(
        _('Type'),
        choices=IP_TYPES,
        default=NGO,
    )

    is_active = models.BooleanField(
        _('Is Active'),
        default=True,
        help_text=_('Is still an active Implementing Partner'),
    )

    def __str__(self):
        return self.name

class FacilityType(models.Model):
    name = models.CharField(
        _('Facility Type Name'),
        max_length=200,
    )

    def __str__(self):
        return self.name.title()


class Facility(models.Model):
    hmis_code = models.CharField(
        _('HMIS Code'),
        max_length=100,
        null=True,
        blank=True
    )
    province = models.ForeignKey(
        Province,
        default="",
        on_delete=models.CASCADE,
        verbose_name=_("Province"),
    )

    district = models.ForeignKey(
        District,
        default=1,
        on_delete=models.CASCADE,
        help_text=_("District in which the facility is located"),
        max_length=250,
    )

    name = models.CharField(
        _('Name'),
        max_length=200,
        help_text=_(
            "Just enter name without 'Hostpial' or 'Clinic`, i.e for `Kitwe General Hospital` just enter `Kitwe General`.")
    )

    facility_type = models.ForeignKey(
        FacilityType,
        default=1,
        on_delete=models.CASCADE,
        help_text=_("Facility Type, i.e 'Hospital, Clinic etc"),
        max_length=250,
    )

    implementing_partner = models.ForeignKey(
        ImplementingPartner,
        on_delete=models.SET_NULL,
        help_text=_("Related Implementing Partner."),
        max_length=250,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'

    def save(self):
        if self.facility_type.name.lower() in self.name.lower():
            self.name = (self.name).title()
        else:
            f"{self.name.title()} {self.facility_type.name.title()}"
        super(Facility, self).save()

    def __str__(self):
        return str(self.name)

class ServiceProviderPersonelQualification(models.Model):
    name = models.CharField(
        max_length=200
    )
    def __str__(self):
        return self.name

class ServiceProviderPersonel(models.Model):
    first_name = models.CharField(
        _("First Name"),
        max_length=200
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=200
    )
    date_of_birth = models.DateField(
        _("Date of Birth"),
        null=True,
        blank=True
    )
    department = models.CharField(
        _("Department"),
        max_length=200,
        null=True,
        blank=True
    )
    facility = models.ForeignKey(
        Facility,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    qualification = models.ForeignKey(
        ServiceProviderPersonelQualification,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    class Meta:
        verbose_name = _("Service Provider")
        verbose_name_plural = _("Service Providers")
    
    def __str__(self):
        return f"Service Provider: {self.first_name} {self.last_name}"
