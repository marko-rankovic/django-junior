from django.contrib.auth.models import User
from django import forms


class ProfileForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']