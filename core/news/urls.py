from django.urls import path

from . import views

app_name = "news"
urlpatterns = [
    path("", views.news, name="news"),
    path("articles/<int:pk>/", views.article, name="article"),
    path("site/<int:pk>/", views.site, name="site"),
]
