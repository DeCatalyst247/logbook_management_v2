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

    return render(
        request,
        "supervision/supervision_dashboard.html",
        {"logs": logs}
    )


def review_log(request, log_id):

    log = get_object_or_404(
        LogEntry,
        id=log_id
    )

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "approve":

            log.status = "approved"

        elif action == "reject":

            log.status = "rejected"

        comment = request.POST.get("comment")
        log.supervisor_comment = comment
        log.save()

        return redirect(
            "supervisor_dashboard"
        )

    return render(
        request,
        "supervision/review_log.html",
        {"log": log}
    )