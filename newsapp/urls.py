from django.urls import path

from . import views

app_name = "newsapp"
urlpatterns = [
    path("", views.posts, name="posts"),
    path("news/", views.news, name="news"),
    path("article/<int:pk>/", views.article, name="article"),
    path("post/<int:pk>/", views.post, name="post"),
    path("comment/<int:pk>/", views.comment, name="comment"),
    path("reply/<int:pk>/", views.reply, name="reply"),
    path("about/", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot/", views.forgot, name="forgot"),
]
