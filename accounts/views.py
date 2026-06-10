# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.decorators import login_required
from logbook.models import LogEntry
from .forms import RegisterForm,ProfileForm
from .models import Profile


def register_view(request):

    form = RegisterForm(
        request.POST or None
    )

    if form.is_valid():

        # SAVE USER
        user = form.save(commit=False)

        # HASH PASSWORD
        user.set_password(
            form.cleaned_data["password"]
        )

        user.save()

        # CREATE PROFILE
        Profile.objects.create(
            user=user,
            role=form.cleaned_data["role"]
        )

        # LOGIN USER
        login(request, user)

        return redirect("dashboard")

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("home")




@login_required
def profile(request):

    profile = request.user.profile

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

    else:

        form = ProfileForm(
            instance=profile
        )

    total_logs = LogEntry.objects.filter(
        student=request.user
    ).count()

    approved_logs = LogEntry.objects.filter(
        student=request.user,
        status="approved"
    ).count()

    pending_logs = LogEntry.objects.filter(
        student=request.user,
        status="pending"
    ).count()

    rejected_logs = LogEntry.objects.filter(
        student=request.user,
        status="rejected"
    ).count()

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "total_logs": total_logs,
            "approved_logs": approved_logs,
            "pending_logs": pending_logs,
            "rejected_logs": rejected_logs,
        }
    )