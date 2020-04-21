from smtplib import SMTPException

from django import http, urls
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .forms import UploadFileForm
from .models import Blob, Receipt
from .utils import send_email


def download_file(request, blob_uuid):
    blob = get_object_or_404(Blob, uuid=blob_uuid)
    key = request.GET.get("key", b"")

    content = blob.decrypt_content(fernet_key=key)
    blob.delete()

    return http.HttpResponse(content, content_type=blob.mimetype)


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            file = form.cleaned_data["file"]

            blob, key = Blob.encrypt_content(
                content=file.read(), mimetype=file.content_type
            )
            blob.save()

            message = f"Decryption key is {key.decode('utf-8')}️"
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

    else:
        form = UploadFileForm()

    is_quota_reached = Receipt.is_quota_reached(date=timezone.now().date())
    return render(
        request, "app/upload.html", {"form": form, "quota_reached": is_quota_reached}
    )
