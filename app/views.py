from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def home(_):
    return HttpResponseRedirect(reverse("posts:latest"))


def about(request):
    return render(request, "about.html", {"page_title": "About"})
