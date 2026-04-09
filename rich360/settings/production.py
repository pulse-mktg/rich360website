import os
import secrets
import dj_database_url
from .base import *

DEBUG = False

# Use env var if set; fall back to a per-process random key.
# NOTE: sessions/cookies will be invalidated on each redeploy when using the
# fallback. Set SECRET_KEY in Railway's Variables tab to avoid this.
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(50)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# Railway injects DATABASE_URL for PostgreSQL; fall back to SQLite locally.
db_url = os.environ.get("DATABASE_URL")
if db_url:
    DATABASES = {
        "default": dj_database_url.parse(db_url, conn_max_age=600, conn_health_checks=True)
    }

# Whitenoise for static files
MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE

STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Wagtail admin base URL
WAGTAILADMIN_BASE_URL = os.environ.get("WAGTAILADMIN_BASE_URL", "https://rich360website.up.railway.app")

# Email (configure in Railway Variables when ready)
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True

CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if host and host != "*"
]

try:
    from .local import *
except ImportError:
    pass
