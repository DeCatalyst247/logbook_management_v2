from django import forms
from .models import LogEntry


class LogEntryForm(forms.ModelForm):

    class Meta:
        model = LogEntry
        fields = [
            "date",
            "title",
            "description",
            "evidence",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_date(self):

        date = self.cleaned_data["date"]

        if self.user:

            exists = LogEntry.objects.filter(
                student=self.user,
                date=date
            ).exists()

            if exists:
                raise forms.ValidationError(
                    "You have already submitted a log for this date."
                )

        return date