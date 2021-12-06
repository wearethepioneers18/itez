from datetime import date
from  django.urls import reverse
from django.contrib.gis.db import models
from django.contrib.gis.db.models import fields
from django.db.models.deletion import SET, SET_NULL
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
    ART_STATUS = (
        ("enrolled", _("Enrolled")),
        ("not_enrolled", _("Not Enrolled")),
    )

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
    art_status = models.CharField(
        _("ART Status"),
        max_length=100,
        null=True,
        blank=True,
        choices=ART_STATUS
    )
    last_vl = models.IntegerField(
        _("Last Viral Load"),
        null=True,
        blank=True
    )
    hiv_status = models.BooleanField(
        _("HIV Status"),
        default=False,
        null=True,
        blank=True
    )
    agent = models.ForeignKey(
        AgentDetail,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    registered_facility = models.ForeignKey(
        'Facility',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="registerd_facility"
    )
    service_facility = models.ForeignKey(
        'Facility',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(_("Date of Birth"))
    marital_status = models.CharField(
        _("Marital Status"),
        choices=MARITAL_STATUS,
        max_length=100,
        null=True,
        blank=True
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
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    education_level = models.CharField(
        _("Education level"),
        max_length=300,
        null=True,
        blank=True,
        choices=EDUCATION_LEVEL
    )
    address = models.TextField(
        _("Address"),
        null=True,
        blank=True,
    )
    alive = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Beneficiary"
        verbose_name_plural = "Beneficiaries"
        ordering = ["created"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        """
        Calculates the Beneficiaries age from birth date.
        """
        days_in_year = 365.2425   
        age = int((date.today() - self.date_of_birth).days / days_in_year)
        return age


    def  get_absolute_url(self):
        return reverse('beneficiary:detail', kwargs={'pk': self.pk})
 


class BeneficiaryParent(models.Model):
    father_first_name = models.CharField(
        _("Father First Name"),
        max_length=200
    )
    father_last_name = models.CharField(
        _("Father Last Name"),
        max_length=250,
        null=True,
        blank=True
    )
    mother_first_name = models.CharField(
        _("Mother First Name"),
        max_length=250,
        null=True,
        blank=True
    )
    mother_last_name = models.CharField(
        _("Mother Last Name"),
        max_length=250,
        null=True,
        blank=True
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

class Drug(models.Model):
    """
    Beneficiary's prescribed Drug. 
    """
    beneficiary = models.ForeignKey(
        Beneficiary,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        _("Drug Name"),
        max_length=200,
        null=True,
        blank=True
    )
    manufacturer = models.DateField(
        _("Drug Manufacturer"),
        auto_created=False,
        null=True,
        blank=True
    )
    expiry_date = models.DateField(
        _("Drug Expiry Date"),
        auto_created=False,
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Prescription(models.Model):
    """
    Beneficiary health Facility Prescription data.
    """
    title = models.CharField(
        _("Prescription Title"),
        max_length=200,
        null=True,
        blank=True
    )
    drugs = models.ManyToManyField(
        Drug
    )
    date = models.DateTimeField(
        auto_now_add=False,
        null=True,
        blank=True
    )
    comment = models.TextField(
        _("Extra Details/Comment"),
        null=True,
        blank=True
    )
    class Meta:
        verbose_name = _("Prescription")
        verbose_name_plural = _("Prescriptions")
    
    def __str__(self):
        return f"{self.title}"

class Lab(models.Model):
    """
    Beneficiary's Lab Tests.
    """
    title = models.CharField(
        _("Lab Diagnosis Title"),
        max_length=200,
        null=True,
        blank=True
    )
    results = models.TextField(
        _("Lab Results"),
        null=True,
        blank=True
    )
    results_status = models.CharField(
        _("Lab Results Status"),
        max_length=200,
        null=True,
        blank=True
    )
    requested_date = models.DateTimeField(
        auto_now_add=False,
        null=True,
        blank=True
    )
    comment = models.TextField(
        _("Extra Details/Comment"),
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _("Lab")
        verbose_name_plural = _("Labs")
    
    def __str__(self):
        return f"Lab: {self.title}"

# HTS = 1
# LAB = 2
# PHARMACY = 3
SERVICE_TYPES =  (
    ("HTS", _('HTS (HIV Testing Services)')),
    ("LAB", _('LAB')),
    ("PHARMACY", _('PHARMACY')),
)

# OPD = 1
# ART = 2
CLIENT_TYPES =  (
    ("OPD", _('OPD (Outpatient Departments )')),
    ("ART", _('ART (Antiretroviral Therapy)')),
)


class Service(models.Model):
    """
    Service provision to Beneficiary.
    """
    title = models.CharField(
        _("Service Title"),
        max_length=255,
    )
    service_personnel = models.ForeignKey(
        ServiceProviderPersonel,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    client_type = models.CharField(
        _("Client Type"),
        max_length=255,
        null=True,
        blank=True,
        choices=CLIENT_TYPES
    )
    service_type = models.CharField(
        _("Service Type"),
        max_length=255,
        null=True,
        blank=True,
        choices=SERVICE_TYPES
    )
    document = models.FileField(
        _("Supporting Document"),
        null=True,
        blank=True,
        upload_to="lab_documents/%Y/%m/%d/"
    )
    datetime = models.DateTimeField(
        auto_now_add=True
    )

    comments = models.TextField(
        _("Comments"),
        null=True,
        blank=True,
        help_text=_("Extra comments if any."),
    )
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title

class MedicalRecord(models.Model):
    """
    Beneficiary's Service.
    """
    beneficiary = models.ForeignKey(
        Beneficiary,
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
    )
    provider_comments = models.TextField(
        _("Extra Details/Comment"),
        null=True,
        blank=True
    )
    interaction_date = models.DateTimeField(
        auto_now_add=False,
        null=True,
        blank=True
    )
    prescription = models.ForeignKey(
        Prescription,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    no_of_days = models.IntegerField(
        _("No of Days"),
        null=True,
        blank=True
    )
    when_to_take = models.TextField(
        _("When to Take"),
        max_length=500,
        null=True,
        blank=True
    )
    lab = models.ForeignKey(
        Lab,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Medical Record")
        verbose_name_plural = _("Medical Records")
    
    def __str__(self):
        return f"Medical Record for: {self.beneficiary}, service: {self.service}"
    
    def  get_absolute_url(self):
        return reverse('beneficiary:detail', kwargs={'pk': self.beneficiary.pk})
