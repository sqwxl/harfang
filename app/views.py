from django.http import HttpResponseRedirect
from django.urls import reverse


def home(_):
    return HttpResponseRedirect(reverse("posts:latest"))
