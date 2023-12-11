from .common import *  # noqa

DEBUG = False

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")
# HOST_SCHEME = "https"
