from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User


@login_required(login_url="/auth/login/")
def index(request):
    return render(
        request,
        "index.html",
    )


def signup(request):
    errors = []
    user_created = False
    if request.POST:
        username = request.POST.get("username", "")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if not username or not email or not password or not confirm_password:
            errors += ["All fields not filed"]

        if password != confirm_password:
            errors += ["Password and Confirm password do not match"]

        if not errors:
            try:
                User.objects.create_user(
                    username=username, email=email, password=password
                )
                user_created = True
            except Exception as ex:
                print(ex)
                errors += ["Invalid username or Password or Username already exits."]
    return render(
        request,
        "registration/signup.html",
        {"user_created": user_created, "errors": errors},
    )
