from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path("news/", views.news, name="news"),
    path("articles/<int:pk>/", views.article, name="article"),
    path("news-site/<int:pk>/", views.news_site, name="news_site"),
    path("users/<str:username>/", views.user, name="user"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot/", views.forgot, name="forgot"),
]
