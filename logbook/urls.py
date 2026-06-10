from django.urls import path

from .views import (
    create_log,
    log_list,
    update_log,
    delete_log,
    log_detail,
    export_pdf,
)

urlpatterns = [

    path(
        "create/",
        create_log,
        name="create_log"
    ),

    path(
        "",
        log_list,
        name="log_list"
    ),

    path(
        "update/<int:pk>/",
        update_log,
        name="update_log"
    ),

    path(
        "delete/<int:pk>/",
        delete_log,
        name="delete_log"
    ),


    path(
        "detail/<int:pk>/",
        log_detail,
        name ="log_detail"
    ),

    path("export-pdf/", export_pdf, name="export_pdf"),
]