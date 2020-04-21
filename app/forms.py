from django import forms


class DownloadFileForm(forms.Form):
    decryption_key = forms.CharField(widget=forms.PasswordInput())


class UploadFileForm(forms.Form):
    email = forms.EmailField()
    file = forms.FileField()
