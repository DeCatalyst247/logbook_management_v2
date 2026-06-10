from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ("student", "Student"),
        ("supervisor", "Supervisor"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    #    related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
 #       default="student"
    )
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_students"
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank= True,
        null= True
    )
    def __str__(self):
        return self.user.username