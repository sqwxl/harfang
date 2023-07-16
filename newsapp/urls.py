from django.urls import path

from . import views

app_name = "newsapp"
urlpatterns = [
    path("", views.submissions, name="submissions"),
    path("submissions/", views.submissions, name="submissions"),
    path("news/", views.news, name="news"),
    path("articles/<int:pk>/", views.article, name="article"),
    path("submissions/<int:pk>/", views.submission, name="submission"),
    path("submissions/<int:pk>/vote/", views.submissions_vote, name="submissions_vote"),
    path("submissions/new/", views.submission_new, name="submission_new"),
    path("comments/<int:pk>/", views.comment, name="comment"),
    path("replies/<int:pk>/", views.reply, name="reply"),
    path("about/", views.about, name="about"),
    path("news-site/<int:pk>/", views.news_site, name="news_site"),
    path("users/<str:username>/", views.user, name="user"),
    path("users/<str:username>/submissions", views.user_submissions, name="user_submissions"),
    path("users/<str:username>/comments", views.user_comments, name="user_comments"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot/", views.forgot, name="forgot"),
]
