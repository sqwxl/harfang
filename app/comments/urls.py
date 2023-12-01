from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:parent_id>/reply/", views.create_reply, name="reply"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/restore/", views.restore, name="restore"),
    path("<int:pk>/vote/", views.vote, name="vote"),
]
