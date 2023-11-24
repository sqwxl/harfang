from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    path("post/", views.post, name="post"),
    path("<int:parent_id>/reply/", views.reply, name="reply"),
    path("<int:pk>/edit/", views.update, name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]
