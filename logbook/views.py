# Create your views here.
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import LogEntry

from .forms import LogEntryForm
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from django.http import HttpResponse



@login_required
def create_log(request):

    form = LogEntryForm(
        request.POST or None,
        request.FILES or None,
        user= request.user
    )

    if request.method == "POST":

        if form.is_valid():

            log = form.save(commit=False)

            log.student = request.user

            existing_log = LogEntry.objects.filter(
                student=request.user,
                date=log.date
            ).exists()

            if existing_log:

                messages.error(
                    request,
                    "You already submitted a log for this date."
                )

            else:

                log.save()

                messages.success(
                    request,
                    "Log submitted successfully."
                )

                return redirect("log_list")

        else:

            print(form.errors)

    return render(
        request,
        "logbook/create_log.html",
        {"form": form}
    )


@login_required
def log_list(request):
    logs = LogEntry.objects.filter(
        student=request.user
    )
    search = request.GET.get(("search"))    
    
    if search:
        logs =logs.filter(title__icontains=search)
    status = request.GET.get("status")
    if status:
        logs = logs.filter(status=status)
    date = request.GET.get("date")   
    if date:
        logs =logs.filter(date=date)   
    total_my_logs = logs.count()
   
    return render(
        request,
        "logbook/log_list.html",
        {
            "logs": logs,
#            "page_obj": page_obj,
            "total_my_logs" :total_my_logs
        }
    )

@login_required
def update_log(request, pk):

    log = get_object_or_404(
        LogEntry,
        pk=pk,
        student=request.user
    )

    form = LogEntryForm(
        request.POST or None,
        request.FILES or None,
        instance=log
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Log updated successfully."
        )

        return redirect("log_list")

    return render(
        request,
        "logbook/update_log.html",
        {
            "form": form
        }
    )


@login_required
def delete_log(request, pk):

    log = get_object_or_404(
        LogEntry,
        pk=pk,
        student=request.user
    )

    if request.method == "POST":

        log.delete()

        messages.success(
            request,
            "Log deleted successfully."
        )

        return redirect("log_list")

    return render(
        request,
        "logbook/delete_log.html",
        {"log": log}
    )

@login_required
def log_detail(request, pk):

    log = get_object_or_404(
        LogEntry,
        pk=pk,
        student=request.user
    )

    return render(request, "logbook/log_detail.html",
    {"log":log})

@login_required
def export_pdf(request):

    logs = LogEntry.objects.filter(student=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="logbook.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.drawString(100, y, "MY IT LOGBOOK REPORT")

    y -= 40

    for log in logs:
        p.drawString(100, y, f"{log.date} - {log.title} - {log.status}")
        y -= 20

    p.showPage()
    p.save()

    return response