from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="/auth/login/")
def index(request):
    return render(
        request,
        "index.html",
    )


def signup(request):
    return render(
        request,
        "registration/signup.html",
    )