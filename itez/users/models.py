from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from itez.beneficiary.models import District
class User(AbstractUser):
    """Default user for ITEZ."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Profile(models.Model):
    """
    A model for storing addtional imformation about User.
    """
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

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    birth_date = models.DateField(
        _("Birth"),
        null=True,
        blank=True
    )
    gender = models.CharField(
        _("Gender"),
        max_length=100,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    sex = models.CharField(
        _("Sex"),
        max_length=100,
        choices=SEX_CHOICES,
        null=True,
        blank=True
    )
    about_me = models.CharField(
        _("About Me"), 
        max_length=300, 
        null=True, 
        blank=True
    )
    education_level = models.CharField(
        _("Education Level"), 
        max_length=200, 
        choices=EDUCATION_LEVEL, 
        null=True, 
        blank=True
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
        max_length=15,
        null=True,
        blank=True
    )
    phone_number_2 = models.CharField(
        _("Phone Number 2"),
        max_length=15,
        null=True,
        blank=True
    )
    address = models.TextField(
        _("Address"),
        max_length=300,
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        if not self.user.name:
            return f"Profile: {self.user.username}"
        return f"Profile: {self.user.name}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class UserWorkDetail(models.Model):
    """
    Include User Work Detail properties.
    """
    company_name = models.CharField(
        _("Company Name"),
        max_length=200,
        null=False,
        blank=True
    )
    work_address = models.TextField(
        _("Work Address"),
        null=True,
        blank=True
    )
    company_phone = models.CharField(
        _("Company Phone number"), 
        max_length=20,
        null=True,
        blank=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_work_detail")

    def __str__(self):
        if not self.user.name:
            return f"Company: {self.company_name}, User: {self.user.username}"
        return f"Company: {self.company_name}, User: {self.user.name}"
