from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", include("core.auth.urls")),
    path("news/", include("core.news.urls")),
    path("submissions/", include("core.submissions.urls")),
    path("users/", include("core.users.urls")),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    #
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
