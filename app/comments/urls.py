from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    # path("<int:pk>/", views.detail, name="detail"), # not implemented (might make sense to combine with reply view)
    path("<int:parent_id>/reply/", views.reply, name="reply"),
    path("<int:pk>/edit/", views.update, name="edit"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]
