from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path(
        "about/", TemplateView.as_view(template_name="about.html"), name="about"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True, next_page="/"
        ),
        name="login",
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
    ),
    path("", views.home, name="home"),
    path("posts/", views.posts_top, name="posts"),
    path("posts/top/", views.posts_top, name="top"),
    path("posts/latest/", views.posts_latest, name="latest"),
    path("posts/<int:pk>/", views.posts_detail, name="post"),
    path("posts/submit/", views.posts_submit, name="submit"),
    path("comments/", include("app.comments.urls")),
    path("votes/posts/<int:pk>", views.post_vote, name="post_vote"),
    path("votes/comments/<int:pk>", views.comment_vote, name="comment_vote"),
    path("users/signup/", views.user_create, name="signup"),
    path("users/<str:username>/", views.user_profile, name="profile"),
    path(
        "users/<str:username>/edit",
        views.user_profile_edit,
        name="profile_edit",
    ),
    path("users/<str:username>/posts/", views.user_posts, name="user_posts"),
    path(
        "users/<str:username>/comments/",
        views.user_comments,
        name="user_comments",
    ),
]
