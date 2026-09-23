from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from logbook.models import LogEntry
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser
@user_passes_test(is_admin)
def admin_dashboard(request):

    context = {

        "students":
        User.objects.count(),

        "logs":
        LogEntry.objects.count(),

        "approved":
        LogEntry.objects.filter(
            status="approved"
        ).count(),

        "pending":
        LogEntry.objects.filter(
            status="pending"
        ).count(),

        "rejected":
        LogEntry.objects.filter(
            status="rejected"
        ).count(),

        "recent_logs":
        LogEntry.objects.order_by(
            "-created_at"
        )[:10]
    }

    return render(
        request,
        "administration/dashboard.html",
        context
    )