# -*- encoding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import RolesManager
from django.urls import reverse
from itez.authentication.forms import LoginForm, SignUpForm, UserCreationForm
from itez.users.models import User
from itez.users.models import Profile
from rolepermissions.checkers import has_role

@login_required(login_url="/login/")
def create_user(request):
    user_form = SignUpForm()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]
        email_address = request.POST.get("email_address", None)
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        gender = request.POST.get("gender", None)
        sex = request.POST.get("sex", None)
        birth_date = request.POST.get("birth_date", None)
        roles_to_assign = request.POST.getlist("user_roles", [])
        if password == password_confirm:
            user_create_object = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email_address,
            )
            
            user_create_object.set_password(password)
            user_create_object.save()
            if roles_to_assign:
                for role in roles_to_assign:
                    if has_role(request.user, [role]):
                        assign_role(user_create_object, role)

            user_create_object.profile.sex = sex
            user_create_object.profile.gender = gender
            if birth_date:
                user_create_object.profile.birth_date = birth_date
            user_create_object.profile.save()
            return redirect("/")
            
        else:  
            return redirect("login/")  
            

    uncleaned_user_roles = RolesManager.get_roles_names()
    cleaned_user_roles = []
    for user_role in uncleaned_user_roles:
        splitted_user_role = user_role.split("_")
        cleaned_user_role = " ".join(splitted_user_role).title()
        cleaned_user_roles.append({
            "key": f"{user_role}",\
            "value": f"{cleaned_user_role}"
        })
    context = {"user_roles": cleaned_user_roles}
    
    html_template = loader.get_template('accounts/register.html')
    return HttpResponse(html_template.render(context, request))

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
