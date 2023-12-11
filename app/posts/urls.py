from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path("", views.top, name="index"),
    path("top/<str:range>/", views.top, name="top"),
    path("latest/", views.latest, name="latest"),
    path("submit/", views.create, name="submit"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/edit/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/vote/", views.vote, name="vote"),
]
