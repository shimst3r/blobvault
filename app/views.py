from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import UploadFileForm
from .models import Blob


def download_file(request, blob_uuid):
    blob = get_object_or_404(Blob, uuid=blob_uuid)
    key = request.GET.get("key", b"")

    content = blob.decrypt_content(fernet_key=key)
    blob.delete()

    # TODO: Get mimetype from Blob model
    return HttpResponse(content, content_type="application/octet-stream")


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            blob, key = Blob.encrypt_content(content=form.cleaned_data["file"].read())
            blob.save()

            message = f"Decryption key is {key.decode('utf-8')}️"
            messages.add_message(request, messages.INFO, message)
            messages.add_message(request, messages.INFO, f"uuid: {blob.pk}")

            return HttpResponseRedirect(reverse("app:upload-file"))

    else:
        form = UploadFileForm()

    return render(request, "app/upload.html", {"form": form})
