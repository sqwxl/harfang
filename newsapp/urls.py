from django.urls import path

from . import views

app_name = "newsapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("article/<int:pk>/", views.article, name="article"),
    path("article/<int:pk>/comments", views.comments, name="comments"),
    path("about/", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot/", views.forgot, name="forgot"),
]
