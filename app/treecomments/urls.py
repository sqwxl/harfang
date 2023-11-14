from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    # path("<int:pk>/", views.detail, name="detail"), # not implemented (might make sense to combine with reply view)
    path("reply/<int:parent_id>", views.reply, name="reply"),
    path("edit/<int:pk>", views.update, name="edit"),
]
