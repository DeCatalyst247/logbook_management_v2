from django.urls import path
from .views import (
    supervisor_dashboard,
    review_log,
)

urlpatterns = [

    path(
        "",
        supervisor_dashboard,
        name="supervisor_dashboard"
    ),

    path(
        "review/<int:log_id>/",
        review_log,
        name="review_log"
    ),
]