from .common import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SECURE = False

if DEBUG:
    try:
        import debug_toolbar  # NOQA
        import django_browser_reload  # NOQA
    except ImportError:
        print("Failed to load debug_toolbar or debug_browser_reload")
    else:
        INSTALLED_APPS.extend(  # noqa: F405
            [
                "debug_toolbar",
                "django_browser_reload",
            ]
        )
        INTERNAL_IPS = ["127.0.0.1"]
        MIDDLEWARE.insert(
            MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        )
        MIDDLEWARE.insert(
            MIDDLEWARE.index("debug_toolbar.middleware.DebugToolbarMiddleware")
            + 1,
            "django_browser_reload.middleware.BrowserReloadMiddleware",
        )
