from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    # NOTE : THIS IS NOT USED... THERE IS NO FORM VALIDATION!!!!
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        #calling super(RegistrationForm) internally calls set_password
        user = super(RegistrationForm,self).save()
        return user

class photoUploadForm(forms.Form):
    userId = forms.IntegerField()
    advId = forms.IntegerField()
    mapId = forms.IntegerField()
    file = forms.FileField()
