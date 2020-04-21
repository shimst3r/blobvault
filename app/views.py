from smtplib import SMTPException

from cryptography import fernet
from django import http, urls, views
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .forms import DownloadFileForm, UploadFileForm
from .models import Blob, Receipt
from .utils import send_email


class DownloadView(views.View):
    form_class = DownloadFileForm
    template_name = "app/download.html"

    def get(self, request, blob_uuid):
        form = self.form_class()

        return render(
            request, self.template_name, {"form": form, "blob_uuid": blob_uuid}
        )

    def post(self, request, blob_uuid):
        blob = get_object_or_404(Blob, uuid=blob_uuid)

        form = self.form_class(request.POST)
        if form.is_valid():
            key = form.cleaned_data["decryption_key"]

            try:
                content = blob.decrypt_content(fernet_key=key)
            except fernet.InvalidToken:
                message = f"Decryption key is invalid."
                messages.add_message(request, messages.ERROR, message)
            else:
                blob.delete()

                return http.HttpResponse(content, content_type=blob.mimetype)

        return http.HttpResponseRedirect(
            urls.reverse("app:download-file", args=[blob_uuid])
        )


class UploadView(views.View):
    form_class = UploadFileForm
    template_name = "app/upload.html"

    def get(self, request):
        form = self.form_class()
        is_quota_reached = Receipt.is_quota_reached(date=timezone.now().date())

        return render(
            request,
            self.template_name,
            {"form": form, "quota_reached": is_quota_reached},
        )

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data["email"]
            file = form.cleaned_data["file"]

            blob, key = Blob.encrypt_content(
                content=file.read(), mimetype=file.content_type
            )
            blob.save()

            message = f"Decryption key is {key}️"
            messages.add_message(request, messages.INFO, message)

            url = request.build_absolute_uri(
                urls.reverse("app:download-file", args=[blob.pk])
            )
            try:
                send_email(email=email, url=url)
            except SMTPException:
                message = f"Sending to {email} unsuccessful."
                messages.add_message(request, messages.ERROR, message)
            else:
                # If the email has been sent successfully, issue a receipt to
                # keep track of the daily SendGrid quota.
                Receipt.objects.create(creation_date=timezone.now())

        return http.HttpResponseRedirect(urls.reverse("app:upload-file"))
