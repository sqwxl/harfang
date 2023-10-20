from django.urls import path

from . import views

app_name = "submissions"
urlpatterns = [
    path("", views.submissions, name="submissions"),
    path("top/", views.submissions, name="submissions"),
    path("<int:pk>/", views.submission, name="submission"),
    path("new/", views.new, name="new"),
]
