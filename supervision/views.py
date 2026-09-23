# Create your views here.
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from .models import *
from logbook.models import LogEntry
from accounts.models import Profile
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required



@login_required
def supervisor_dashboard(request):

    logs = LogEntry.objects.all().order_by("-created_at")
    
    q = request.GET.get("q")
    if q:
        logs = logs.filter(
            Q(title__icontains=q)

            |

            Q(student__username__icontains=q)

        )
    search = request.GET.get("search")

    if search:
        logs = logs.filter(
        studentusernameicontains=search
    )
    pending_reviews = LogEntry.objects.filter(
    status="pending"
).count()

    approved_logs = LogEntry.objects.filter(
    status="approved"
).count()

    rejected_logs = LogEntry.objects.filter(
    status="rejected"
).count()
    return render(
        request,
        "supervision/supervision_dashboard.html",
        {
            "logs": logs,
            "pending_reviews":pending_reviews,
            "approved_logs":approved_logs,
            "rejected_logs":rejected_logs,

        }
    )

def review_log(request, log_id):

    log = get_object_or_404(LogEntry, id=log_id)

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "approve":
            log.status = "approved"

        elif action == "reject":
            log.status = "rejected"

        comment = request.POST.get("comment")
        log.supervisor_comment = comment
        log.save()

        # EMAIL PART
        if log.student.email:

            try:
                send_mail(
                    subject="IT Logbook - Logbook Review Notification",
                    message=f"""
Hello {log.student.username},

Your log entry title:
"{log.title}"
has been {log.status.upper()}.

Supervisor Comment:
{comment}

Thank you for using the IT Logbook Management System

Regards,
Catalyst
IT Logbook Management System
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[log.student.email],
                    fail_silently=False,
                )

            except Exception as e:
                print("Email error:", e)

        return redirect("supervisor_dashboard")

    return render(request, "supervision/review_log.html", {"log": log})