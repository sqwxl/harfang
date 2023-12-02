from .common import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

ENABLE_DEBUG_TOOLBAR = False

if DEBUG:
    if ENABLE_DEBUG_TOOLBAR:
        try:
            import debug_toolbar  # NOQA
        except ImportError:
            print("Failed to load debug_toolbar")
        else:
            INSTALLED_APPS.extend(["debug_toolbar"])
            MIDDLEWARE.insert(
                MIDDLEWARE.index("django.middleware.common.CommonMiddleware")
                + 1,
                "debug_toolbar.middleware.DebugToolbarMiddleware",
            )
            INTERNAL_IPS = ["127.0.0.1"]
            # https://django-debug-toolbar.readthedocs.io/en/latest/tips.html#working-with-htmx-and-turbo
            DEBUG_TOOLBAR_CONFIG = {"ROOT_TAG_EXTRA_ATTRS": "hx-preserve"}

    try:
        import django_browser_reload  # NOQA
    except ImportError:
        print("Failed to load django_browser_reload")
    else:
        INSTALLED_APPS.extend(["django_browser_reload"])
        MIDDLEWARE.insert(
            MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
            "django_browser_reload.middleware.BrowserReloadMiddleware",
        )
