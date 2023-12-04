from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("posts/", include("app.posts.urls")),
    path("comments/", include("app.comments.urls")),
    path("users/", include("app.users.urls")),
    path(
        "about/", TemplateView.as_view(template_name="about.html"), name="about"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True,
            next_page="/",
        ),
        name="login",
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"
    ),
]
