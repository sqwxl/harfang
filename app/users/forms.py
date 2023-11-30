from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

    bio = forms.CharField(widget=forms.Textarea)
