from .common import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SECURE = False

if DEBUG:
    try:
        import debug_browser_reload  # noqa: F401
        import debug_toolbar  # noqa: F401
    except ImportError:
        pass
    else:
        INSTALLED_APPS.extend(  # noqa: F405
            [
                "debug_toolbar",
                "debug_browser_reload",
            ]
        )
        INTERNAL_IPS = ["127.0.0.1"]
        MIDDLEWARE.insert(
            MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        )
        MIDDLEWARE.insert(
            MIDDLEWARE.index("debug_toolbar.middleware.DebugToolbarMiddleware") + 1,
            "djangoproject.middleware.CORSMiddleware",
        )
        MIDDLEWARE.insert(
            MIDDLEWARE.index("debug_toolbar.middleware.DebugToolbarMiddleware") + 1,
            "django_browser_reload.middleware.BrowserReloadMiddleware",
        )
