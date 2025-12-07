from django.shortcuts import render, HttpResponse, redirect
import json
from account.models import Student, Expert
from account.choices import UserTypeChoices
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

def signup_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if not password1 or not password2:
            messages.error("Passwords do not match")
            return redirect("signup")

        user_type = request.POST.get("user_type")
        UserModel = [Student, Expert][user_type == UserTypeChoices.expert]
        try:
            user = UserModel.objects.get(email=email)
        except Exception as e:
            user = None
        if user:
            messages.error(request, f"User email {email} already exists")
            return redirect("signup")
        user = UserModel.objects.create_user(email=email, password=password1)
        login(request, user)
        return redirect("home")
    context = {"user_type": UserTypeChoices.student}
    return render(request, "account/signup.html", context=context)


def login_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(f"Email and passowrd are required")
            return redirect("login")

        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
    return render(request, "account/login.html", )


def logout_view(request, *args, **kwargs):
    if request.user.is_authenticated :
        logout(request)
    else :
        messages.error(request , "You are not authenticated !")
    return redirect("home")
