from django.urls import include, path

from . import views

app_name = "comments"
urlpatterns = [
    path("", include("django_comments.urls")),
    # path("new/<int:object_id>/", views.create, name="new"),
    # path("<int:pk>/", views.detail, name="detail"), # not implemented (might make sense to combine with reply view)
    path("reply/<int:parent_comment_id>", views.reply, name="reply"),
    path("edit/<int:pk>", views.update, name="edit"),
]
