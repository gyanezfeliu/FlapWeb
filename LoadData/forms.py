from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.models import User
from LoadData.models import UserProfileInfo, Experiment, Sample, Dna, Measurement, Inducer

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

class MediaModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.media)

class StrainModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.strain)

class SearchForm(forms.Form):
    experiment = forms.ModelChoiceField(queryset=Experiment.objects.all().order_by('name'), empty_label="All", required=False)
    dna = forms.ModelChoiceField(queryset=Dna.objects.all().order_by('name'), empty_label="All", required=False)
    media = MediaModelChoiceField(queryset=Sample.objects.distinct('media'), empty_label="All", required=False)
    strain = StrainModelChoiceField(queryset=Sample.objects.distinct('strain'), empty_label="All", required=False)
    inducer = forms.ModelChoiceField(queryset=Inducer.objects.distinct('pubchemid'), empty_label="All", required=False)
    measurement_name = forms.ModelChoiceField(queryset=Measurement.objects.distinct('name'), empty_label="All", required=False)
