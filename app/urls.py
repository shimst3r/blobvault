from django.urls import path

from .views import download_file, upload_file

app_name = "app"
urlpatterns = [
    path("<uuid:blob_uuid>", download_file, name="download-file"),
    path("", upload_file, name="upload-file"),
]
