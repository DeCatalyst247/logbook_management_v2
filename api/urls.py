from django.urls import path

from .views import logs_api

urlpatterns = [

    path(
        "logs/",
        logs_api,
        name="logs_api"
    )
]