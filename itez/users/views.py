from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from itez.users.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from itez.users.models import User as user_model
from itez.users.models import Profile
from itez.beneficiary.models import District, Province
from itez.users.models import EDUCATION_LEVEL, GENDER_CHOICES, SEX_CHOICES

User = get_user_model()


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


@login_required(login_url="/login/")
def user_profile(request):
    user_profile = Profile.objects.get(id=request.user.id)
    current_user = user_model.objects.get(id=request.user.id)
    user_district = District.objects.get(id=request.user.id)
    user_province = Province.objects.get(id=request.user.id)
    if request.method == "POST":
        phone_no_1 = request.POST.get("phone-no-1", user_profile.phone_number)
        phone_no_2 = request.POST.get("phone-no-2", user_profile.phone_number_2)
        first_name = request.POST.get("first-name", user_profile.user.first_name)
        last_name = request.POST.get("last-name", user_profile.user.last_name)
        username = request.POST.get("username", user_profile.user.username)
        address = request.POST.get("address", user_profile.address)
        postal_code = request.POST.get("postal-code", user_profile.postal_code)
        province = request.POST.get("province", user_province.name)
        district = request.POST.get("district", user_district.name)
        email = request.POST.get("email", user_profile.user.email)
        gender = request.POST.get("gender", user_profile.gender)
        sex = request.POST.get("sex", user_profile.sex)
        profile_photo = request.FILES.get("profile-photo", user_profile.profile_photo)
        education_level = request.POST.get(
            "education-level", user_profile.education_level
        )
        about = request.POST.get("about", user_profile.about_me)
        birth_date = request.POST.get("birth-date", user_profile.birth_date)
        if birth_date:
            user_profile.birth_date = birth_date

        user_profile.phone_number = phone_no_1
        user_profile.phone_number_2 = phone_no_2
        user_profile.address = address
        user_profile.postal_code = postal_code
        user_profile.gender = gender
        user_profile.sex = sex
        user_profile.education_level = education_level.title()
        user_profile.about_me = about
        user_profile.profile_photo = profile_photo
        user_profile.save()

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        current_user.username = username
        current_user.save()

        user_district.name = district
        user_district.save()

        user_province.name = province
        user_province.save()
        return redirect("/user/profile")

    education_levels = [level[1] for level in EDUCATION_LEVELS]
    sex_array = [sex[1] for sex in SEX_CHOICES]
    gender_array = [gender[1] for gender in GENDER_CHOICES]
    
    context = {
        "province": user_province,
        "user": user_profile,
        "education_levels": education_levels,
        "gender_array": gender_array,
        "sex_array": sex_array,
    }
    return render(request, "includes/user_profile.html", context)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
