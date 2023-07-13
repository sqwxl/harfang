from django.urls import path

from . import views

app_name = "newsapp"
urlpatterns = [
    path("", views.posts, name="posts"),
    path("news/", views.news, name="news"),
    path("article/<int:pk>/", views.article, name="article"),
    path("post/<int:pk>/", views.post, name="post"),
    path("post/new/", views.post_new, name="post-new"),
    path("comment/<int:pk>/", views.comment, name="comment"),
    path("reply/<int:pk>/", views.reply, name="reply"),
    path("about/", views.about, name="about"),
    path("user/<str:username>/", views.user, name="user"),
    path("user/<str:username>/posts", views.user, {"items": "posts"}, name="user-posts"),
    path("user/<str:username>/comments", views.user, {"items": "comments"}, name="user-comments"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot/", views.forgot, name="forgot"),
]
