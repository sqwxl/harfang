from django.urls import path

from . import views

app_name = "comments"
urlpatterns = [
    path("create/<str:app_label>/<str:model_name>/<int:object_id>/", views.create_view, name="create"),
    path("reply/<int:pk>/", views.reply_view, name="reply"),
]
