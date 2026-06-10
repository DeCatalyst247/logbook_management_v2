from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from logbook.models import LogEntry

from .serializers import (
    LogEntrySerializer
)




@api_view(["GET"])
def logs_api(request):

    logs = LogEntry.objects.all()

    serializer = LogEntrySerializer(
        logs,
        many=True
    )

    return Response(
        serializer.data
    )