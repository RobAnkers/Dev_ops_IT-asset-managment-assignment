# settings.py

"""
Django settings for inventory_management project.
"""

import dj_database_url
import os
import environ
from pathlib import Path
from decouple import config
from django.conf.global_settings import SECRET_KEY

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()

# Read .env file for sensitive and environment-specific settings.
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY is fetched from the .env file for security purposes.
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG mode should be set to False in production for security reasons.
DEBUG = config('DEBUG', cast=bool)

# Allowed hosts specify the domains or IP addresses this Django site can serve.
ALLOWED_HOSTS = [
    'dev-ops-it-asset-managment-assignment.onrender.com',  # Deployment domain
    '127.0.0.1',  # Localhost for development
    'localhost'  # Alias for localhost
]

# Application definition
# Core Django applications and third-party apps are added here.
INSTALLED_APPS = [
    "django.contrib.admin",  # Admin interface
    "django.contrib.auth",  # Authentication system
    "django.contrib.contenttypes",  # Content type framework
    "django.contrib.sessions",  # Session management
    "django.contrib.messages",  # Messaging framework
    "django.contrib.staticfiles",  # Static files management
    "inventory",  # Custom app for inventory management
    "crispy_forms",  # Enhanced form handling
    "crispy_bootstrap5",  # Bootstrap 5 templates for crispy_forms
]

# Middleware is processed in the listed order to handle requests and responses.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Basic security enhancements
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',  # Common HTTP features
    'django.middleware.csrf.CsrfViewMiddleware',  # Cross-Site Request Forgery protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protect against clickjacking
]

# Root URL configuration module
ROOT_URLCONF = "inventory_management.urls"

# Template configuration
# Configures Django's template engine to locate and render templates.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Additional directories for templates
        "APP_DIRS": True,  # Enable app-specific templates
        "OPTIONS": {
            "context_processors": [  # Context processors add variables to template contexts
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application entry point
WSGI_APPLICATION = "inventory_management.wsgi.application"

# Database configuration
# Using dj-database-url to parse DATABASE_URL from .env file for flexibility.
DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL'))
}

# Password validation settings
# Add multiple password validators for improved security.
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
# Set default language and timezone.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True  # Enable internationalization features
USE_TZ = True  # Enable timezone support

# Static files configuration
# Configure static files handling, including storage and paths.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # Use WhiteNoise for serving
                                                                                # static files in production
STATIC_URL = "/static/"  # URL prefix for static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Additional static files directories
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory where static files will be collected for deployment

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # Default field type for model primary keys

# Third-party app settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # Specify allowed template packs for crispy_forms
CRISPY_TEMPLATE_PACK = "bootstrap5"  # Use Bootstrap 5 for form rendering

# Authentication settings
LOGIN_REDIRECT_URL = '/dashboard'  # Redirect users to the dashboard after login
LOGIN_URL = 'login'  # URL for the login view

# Application-specific settings
LOW_QUANTITY = 3  # Threshold for low inventory quantity alerts



