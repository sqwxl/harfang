from django.contrib.auth import forms, get_user_model
from django.forms import ModelForm

from .models import Post, Profile


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = forms.UserCreationForm.Meta.fields


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "url", "body"]
