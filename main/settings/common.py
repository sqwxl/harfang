import os
from pathlib import Path

PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

BASE_DIR = PROJECT_PACKAGE.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "whatever")

X_FRAME_OPTIONS = "DENY"

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "treecomments",
    "submissions",
    "news",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compressor",
    "mptt",
    "widget_tweaks",
    "django_comments",
]

# https://django-contrib-comments.readthedocs.io/en/latest/custom.html#customizing-the-comments-framework
COMMENTS_APP = "treecomments"
COMMENTS_ALLOW_PROFANITIES = False

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_PACKAGE / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATICFILES_DIRS = [PROJECT_PACKAGE / "static"]

STATIC_URL = "static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

COMPRESS_ENABLED = True

STATIC_ROOT = BASE_DIR / "_static"

MEDIA_ROOT = BASE_DIR / "_media"

# https://django-debug-toolbar.readthedocs.io/en/latest/tips.html#working-with-htmx-and-turbo
DEBUG_TOOLBAR_CONFIG = {"ROOT_TAG_EXTRA_ATTRS": "hx-preserve"}

PROFANITIES_LIST = [
    "beaner",
    "chinaman",
    "ching chong",
    "chink",
    "coon",
    "coonass",
    "cunt",
    "darkie",
    "darky",
    "eskimo",
    "fag",
    "faggot",
    "gook",
    "half-breed",
    "jigaboo",
    "jiggabo",
    "jigger",
    "kike",
    "kyke",
    "midget",
    "muzzie",
    "nigga",
    "nigger",
    "paki",
    "pakkis",
    "polack",
    "polak",
    "raghead",
    "retard",
    "retarded",
    "shemale",
    "slanteye",
    "tacohead",
    "tar-baby",
    "tard",
    "towel head",
    "tranny",
    "wetback",
]
