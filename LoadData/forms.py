from django import forms
from django.contrib.auth.models import User
from LoadData.models import UserProfileInfo

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    dataFile = forms.FileField()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
