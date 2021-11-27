from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from itez.users.forms import UserChangeForm, UserCreationForm
from .models import Profile, UserWorkDetail, User


# User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile)
admin.site.register(UserWorkDetail)