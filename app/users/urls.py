from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.create, name="create"),
    path("<str:username>/", views.profile, name="profile"),
    path("<str:username>/edit", views.profile_edit, name="profile_edit"),
    path("<str:username>/posts/", views.posts, name="posts"),
    path("<str:username>/comments/", views.comments, name="comments"),
]
