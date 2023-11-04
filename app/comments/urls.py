from django.urls import include, path

from . import views

app_name = "comments"
urlpatterns = [
    path("", include("django_comment.urls")),
    path("<str:username>/", views.list_for_user, name="list"),  # TODO: remove
    path("tree/<int:object_id>/", views.tree, name="tree"),
    path("new/<int:object_id>/", views.create, name="new"),
    # path("<int:pk>/", views.detail, name="detail"), # not implemented (might make sense to combine with reply view)
    path("<int:pk>/reply", views.reply, name="reply"),
    path("<int:pk>/edit", views.update, name="edit"),
]
