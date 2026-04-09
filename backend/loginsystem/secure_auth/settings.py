# secure_auth/settings.py

from pathlib import Path
import os
from decouple import config
import dj_database_url
from dotenv import load_dotenv

# ---------- BASE DIRECTORY ----------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# ---------- SECURITY ----------
SECRET_KEY = config('SECRET_KEY', default='replace-me-with-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)

# ---------- HOSTS ----------
ALLOWED_HOSTS = [host.strip() for host in config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')]

# ---------- INSTALLED APPS ----------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'accounts',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'whitenoise.runserver_nostatic',  # Static files in production
]

# ---------- MIDDLEWARE ----------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------- URL CONFIG ----------
ROOT_URLCONF = 'secure_auth.urls'

# ---------- TEMPLATES ----------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'secure_auth.wsgi.application'

# ---------- DATABASE ----------
DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3')),
        conn_max_age=600,
        ssl_require=False  # False for dev; set True for hosted Postgres
    )
}

# ---------- PASSWORD VALIDATORS ----------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------- INTERNATIONALIZATION ----------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------- STATIC FILES ----------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------- REST FRAMEWORK ----------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# ---------- CORS ----------
cors_origins_env = config('CORS_ALLOWED_ORIGINS', default='')
if cors_origins_env:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(',')]
else:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

# ---------- PRODUCTION SECURITY ----------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # CSRF_TRUSTED_ORIGINS must include scheme (http:// or https://)
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host != '*']
else:
    # Dev CSRF trusted origins
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]