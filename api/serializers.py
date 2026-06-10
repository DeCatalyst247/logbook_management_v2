from rest_framework import serializers
from logbook.models import LogEntry



class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model= LogEntry
        fields = "__all__"