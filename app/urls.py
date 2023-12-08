from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import home, about

urlpatterns = [
    path("", home, name="home"),
    path("posts/", include("app.posts.urls")),
    path("comments/", include("app.comments.urls")),
    path("users/", include("app.users.urls")),
    path("metadata/", include("app.metadata.urls")),
    path("about/", about, name="about"),
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
