from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    path("post/", views.post, name="post"),
    path("<int:parent_id>/reply/", views.reply, name="reply"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/restore/", views.restore, name="restore"),
]
