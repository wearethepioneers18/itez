from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from itez.beneficiary.models import District


from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, username, password, email=None, **kwargs):
        """Create and return a `User` with an email, username and password."""
        if not username:
            raise TypeError("Users must have a username.")

        if not password:
            raise TypeError("User must have a  papssword.")

        user = self.model(
            username=username, password=password, email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, email=None, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if not password:
            raise TypeError("Superusers must have a password.")
        # if email is None:
        #     raise TypeError("Superusers may have an email.")
        if not username:
            raise TypeError("Superusers must have a unique username.")

        user = self.create_user(
            username=username, password=password, email=email, **kwargs
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, unique=True, max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(db_index=False, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("user:profile", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


EDUCATION_LEVEL = (
    ("none", ("None")),
    ("primary", ("Primary")),
    ("basic", ("Basic")),
    ("secondary", ("Secondary O'Level")),
    ("certificate", ("Certificate")),
    ("diploma", ("Diploma")),
    ("degree", ("Degree")),
    ("masters", ("Masters")),
    ("doctrate", ("Doctrate")),
    ("phd", ("PHD")),
)
GENDER_CHOICES = (
    ("Male", ("Male")),
    ("Female", ("Female")),
    ("Transgender", ("Transgender")),
    ("Other", ("Other")),
)
SEX_CHOICES = (("Male", ("Male")), ("Female", ("Female")))


class Profile(models.Model):
    """
    A model for storing addtional imformation about User.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(_("Birth"), null=True, blank=True)
    gender = models.CharField(
        _("Gender"), max_length=100, choices=GENDER_CHOICES, null=True, blank=True
    )
    sex = models.CharField(
        _("Sex"), max_length=100, choices=SEX_CHOICES, null=True, blank=True
    )
    about_me = models.CharField(_("About Me"), max_length=300, null=True, blank=True)
    education_level = models.CharField(
        _("Education Level"),
        max_length=200,
        choices=EDUCATION_LEVEL,
        null=True,
        blank=True,
    )
    profile_photo = ProcessedImageField(
        upload_to="profile_photo",
        processors=[ResizeToFill(512, 512)],
        format="JPEG",
        options={"quality": 100},
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        _("Phone Number"), max_length=15, null=True, blank=True
    )
    phone_number_2 = models.CharField(
        _("Phone Number 2"), max_length=15, null=True, blank=True
    )
    address = models.TextField(_("Address"), max_length=300, null=True, blank=True)
    city = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = models.CharField(
        _("Postal Code"), max_length=100, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class UserWorkDetail(models.Model):
    """
    Include User Work Detail properties.
    """

    company_name = models.CharField(
        _("Company Name"), max_length=200, null=False, blank=True
    )
    work_address = models.TextField(_("Work Address"), null=True, blank=True)
    company_phone = models.CharField(
        _("Company Phone number"), max_length=20, null=True, blank=True
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_work_detail"
    )

    def __str__(self):
        if not self.user.name:
            return f"Company: {self.company_name}, User: {self.user.username}"
        return f"Company: {self.company_name}, User: {self.user.name}"
