from django.urls import path

from . import views

app_name = "markdown"
urlpatterns = [path("html/", views.to_html, name="to_html")]
