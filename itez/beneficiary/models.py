from django.contrib.gis.db import models
from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.utils.translation import gettext_lazy as _
from .utils import generate_uuid_and_agent_code


GENDER_CHOICES = (
    ("Male", _("Male")),
    ("Female", _("Female")),
    ("Transgender", _("Transgender")),
    ("Other", _("Other"))
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
    agend_ID = models.CharField(
        _("Agent Id"),
        default=generate_uuid_and_agent_code()[1],
        max_length=100
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
    profile_photo = models.ImageField(
        _("Profile Photo"),
        upload_to="profile_photo/",
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
    beneficiary_ID = models.UUIDField(
        default=generate_uuid_and_agent_code()[0],
        editable=False
    )
    agent_ID = models.ForeignKey(
        AgentDetail,
        on_delete=models.PROTECT,
        default=generate_uuid_and_agent_code()[1]
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

    def __str__(self):
        return self.company
