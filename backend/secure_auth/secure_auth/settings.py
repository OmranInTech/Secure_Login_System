from pathlib import Path
import os
from decouple import config
import dj_database_url

# Base project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- SECURITY ----------
SECRET_KEY = config('SECRET_KEY')  # Load from .env
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = [
    'your-backend.onrender.com',  # Replace with your deployed backend URL
]

# ---------- INSTALLED APPS ----------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',  # your app
    'rest_framework',
    'rest_framework_simplejwt',  # JWT auth
    'corsheaders',  # allow React frontend
]

# ---------- MIDDLEWARE ----------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serve static files in production
    'corsheaders.middleware.CorsMiddleware',       # enable CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------- URLS ----------
ROOT_URLCONF = 'secure_auth.urls'

# ---------- TEMPLATES ----------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # add templates folder if needed
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
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# ---------- PASSWORD VALIDATION ----------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ---------- INTERNATIONALIZATION ----------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------- STATIC FILES ----------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # collectstatic folder
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------- REST FRAMEWORK ----------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # secure by default
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # use JWT
    ],
}

# ---------- CORS ----------
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.netlify.app",  # replace with deployed frontend
]