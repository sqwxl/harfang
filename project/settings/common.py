import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "whatever")

X_FRAME_OPTIONS = "DENY"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    # "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms",
    # 3rd-party apps
    "mptt",
    "django_extensions",
    "django_htmx",
    "template_partials",
    # apps
    "app",
    "app.comments",
    "app.posts",
    "app.markdown",
    "app.metadata",
    "app.users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [
                "django.templatetags.i18n",
                "template_partials.templatetags.partials",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
USE_I18N = True
TIME_ZONE = "UTC"
USE_TZ = True
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_URL = "static/"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATIC_ROOT = BASE_DIR / "_static"
MEDIA_ROOT = BASE_DIR / "_media"

COMMENTS_ALLOW_PROFANITIES = False
PROFANITIES_LIST = []
with open(BASE_DIR / "profanities.txt") as f:
    for line in f:
        PROFANITIES_LIST.append(line.strip())

BIO_MAX_LENGTH = 500
POST_TITLE_MAX_LENGTH = 200
POST_URL_MAX_LENGTH = 255
POST_BODY_MAX_LENGTH = 10000
COMMENT_BODY_MAX_LENGTH = 4000

METADATA_SCRAPER_TIMEOUT = 5

# https://python-markdown.github.io/extensions/
MARKDOWN_EXTENSIONS = ["fenced_code", "codehilite"]
# TODO: add css for codehilite https://python-markdown.github.io/extensions/code_hilite/
MARKDOWN_EXTENSION_CONFIGS = dict()

BLEACH_ALLOWED_PROTOCOLS = ["http", "https", "mailto"]
