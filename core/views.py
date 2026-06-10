from django.shortcuts import render
from logbook.models import LogEntry
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.decorators import login_required


def home(request):
    total_students = User.objects.count()
    total_logs = LogEntry.objects.count()
    approved_logs = LogEntry.objects.filter(
        status = "approved"
    ).count()
    pending_logs = LogEntry.objects.filter(
        status ="pending"
    ).count()
    rejected_logs = LogEntry.objects.filter(
    status="rejected"
    ).count()
    context = {
        "total_students": total_students,
        "total_logs": total_logs,
        "approved_logs": approved_logs,
        "pending_logs" : pending_logs,
        "rejected_logs" : rejected_logs,

    }

    return render(
        request,
        "core/home.html",
        context
    )

@login_required
def dashboard(request):

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

    context = {

        "total_logs": total_logs,

        "approved_logs": approved_logs,

        "pending_logs": pending_logs,

        "rejected_logs": rejected_logs,

    }

    return render(
        request,
        "core/dashboard.html",
        context
    )