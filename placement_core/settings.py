"""
Django settings for placement_core project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-iitb-placement-portal-secret-key-production-ready'

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost',
    'http://127.0.0.1',
]

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SESSION_SAVE_EVERY_REQUEST = True
CSRF_FAILURE_VIEW = 'students.views.custom_csrf_failure_view'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'students',
    'recruiters',
    'tpo_officer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'placement_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'students.context_processors.student_notification_context',
                'tpo_officer.context_processors.tpo_context',
                'recruiters.context_processors.recruiter_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'placement_core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Fast Console Email Backend for Automated Notifications & Auditing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'A2Z Placement Cell <placement-cell@a2z.edu.in>'

from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
}

# ==============================================================================
# 📧 REAL EMAIL / GMAIL SMTP OTP CONFIGURATION
# ==============================================================================
# OTP थेट विद्यार्थ्याच्या खऱ्या ईमेलवर (Inbox मध्ये) जाण्यासाठी खालील सेटिंग्ज वापरा:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'borudegaurav7@gmail.com')       # 👈 तुमचा Gmail Email ID
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'bjwo xklu ajfu ryzy')  # 👈 16-अंकी Google App Password
DEFAULT_FROM_EMAIL = f'A2Z Placement Cell <{EMAIL_HOST_USER}>'

# ==============================================================================
# 💬 WHATSAPP NOTIFICATION CONFIGURATION (Twilio / Meta Cloud / UltraMsg)
# ==============================================================================
# विद्यार्थ्यांच्या WhatsApp वर OTP व ऍलर्ट मेसेज पाठवण्यासाठी खालील की टाका:
WHATSAPP_ENABLED = True

# 1. Twilio WhatsApp API (https://www.twilio.com/console)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'your-twilio-account-sid')       # 👈 Twilio Account SID
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'your-twilio-auth-token')          # 👈 Twilio Auth Token
TWILIO_WHATSAPP_FROM = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')   # 👈 Twilio WhatsApp Number

# 2. किंवा UltraMsg API (https://ultramsg.com - popular in India)
ULTRAMSG_INSTANCE_ID = os.environ.get('ULTRAMSG_INSTANCE_ID', 'instanceXXXX')              # 👈 UltraMsg Instance ID
ULTRAMSG_TOKEN = os.environ.get('ULTRAMSG_TOKEN', 'your-ultramsg-token')                   # 👈 UltraMsg Token


