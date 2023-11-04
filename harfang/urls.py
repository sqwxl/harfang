from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    # app
    path("", include("app.urls")),
    #
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
