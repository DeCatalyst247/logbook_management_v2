# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class LogEntry(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='log_entry'
    )

    date = models.DateField()

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()
    supervisor_comment = models.TextField(
        blank = True,
        null= True
    )
    evidence = models.FileField(
        upload_to="evidence/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-date"]

        unique_together = ("student", "date")

    def __str__(self):

        return f"{self.student.username} - {self.date}"


