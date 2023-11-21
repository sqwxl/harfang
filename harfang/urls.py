from django.contrib import admin
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
]

if settings.DEBUG:
    urlpatterns.extend(
        [
            path("__debug__/", include("debug_toolbar.urls")),
            path("__reload__/", include("django_browser_reload.urls")),
        ]
    )
