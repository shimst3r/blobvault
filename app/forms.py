from django import forms


class UploadFileForm(forms.Form):
    email = forms.EmailField()
    file = forms.FileField()
