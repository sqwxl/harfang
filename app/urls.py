from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("", views.home, name="home"),
    path("posts/", views.posts_top, name="posts"),
    path("posts/top/", views.posts_top, name="top"),
    path("posts/latest/", views.posts_latest, name="latest"),
    path("posts/<int:pk>/", views.posts_detail, name="post"),
    path("posts/submit/", views.posts_submit, name="submit"),
    path("comments/", include("app.comments.urls")),
    path("users/create/", views.user_create, name="user_create"),
    path("users/<str:username>/", views.user_detail, name="profile"),
    path("users/<str:username>/posts/", views.user_posts, name="user_posts"),
    path("users/<str:username>/comments/", views.user_comments, name="user_comments"),
]
