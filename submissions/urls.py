from django.urls import path

from . import views

app_name = "submissions"
urlpatterns = [
    path("", views.submissions, name="submissions"),
    path("submissions/", views.submissions, name="submissions"),
    path("submissions/top/", views.submissions, name="submissions"),
    path("submissions/form/", views.submission_form, name="submission_form"),
    path("submissions/<int:pk>/", views.submission, name="submission"),
]
