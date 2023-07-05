from django.urls import path

from . import views

app_name = "newsapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("article/<int:pk>/", views.article, name="article"),
    path("about/", views.about, name="about"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("forgot/", views.forgot, name="forgot"),
]
