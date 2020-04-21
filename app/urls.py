from django.urls import path

from .views import DownloadView, UploadView

app_name = "app"
urlpatterns = [
    path("<uuid:blob_uuid>", DownloadView.as_view(), name="download-file"),
    path("", UploadView.as_view(), name="upload-file"),
]
