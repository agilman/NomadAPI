from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        #calling super(RegistrationForm) internally calls set_password
        user = super(RegistrationForm,self).save()

        #create directory for user media
        #target = settings.USER_MEDIA_ROOT+'/'+str(user.id)
        #target2 = target + "/profile_pictures"
        #os.mkdir(target)
        #os.mkdir(target2)

        return user

class photoUploadForm(forms.Form):
    userId = forms.IntegerField()
    advId = forms.IntegerField()
    mapId = forms.IntegerField()
    file = forms.FileField()
