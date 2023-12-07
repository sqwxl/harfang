from django.urls import path

from . import views

app_name = "metadata"
urlpatterns = [path("url/", views.scrape, name="scrape")]
