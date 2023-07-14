from django.urls import path

from . import views

app_name = "newsapp"
urlpatterns = [
    path("", views.posts, name="posts"),
    path("news/", views.news, name="news"),
    path("articles/<int:pk>/", views.article, name="article"),
    path("posts/<int:pk>/", views.post, name="post"),
    path("posts/new/", views.post_new, name="post-new"),
    path("comments/<int:pk>/", views.comment, name="comment"),
    path("replies/<int:pk>/", views.reply, name="reply"),
    path("about/", views.about, name="about"),
    path("news-site/<int:pk>/", views.news_site, name="news_site"),
    path("users/<str:username>/", views.user, name="user"),
    path("users/<str:username>/posts", views.user_posts, name="user-posts"),
    path("users/<str:username>/comments", views.user_comments, name="user-comments"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot/", views.forgot, name="forgot"),
]
