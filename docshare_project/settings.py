from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^!o3q_=xn$g8&(qwvepf%f_$qv@-8dc_lh_81v^r!@%_le4dky'

DEBUG = True

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', '.ngrok-free.app', '.ngrok.io', '.serveo.net', '.hf.space']

# Support pour ngrok (évite les erreurs CSRF)
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok.io',
    'https://*.serveo.net',
    'https://*.hf.space',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # ton app principale
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'docshare_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # ✅ CORRECTION 1 : dire à Django où trouver les templates
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'docshare_project.wsgi.application'

# Utilisation du volume persistant sur Hugging Face si disponible
PERSISTENT_DATA_DIR = Path('/data')

if PERSISTENT_DATA_DIR.exists():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': PERSISTENT_DATA_DIR / 'db.sqlite3',
        }
    }
    MEDIA_ROOT = PERSISTENT_DATA_DIR / 'media'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    MEDIA_ROOT = BASE_DIR / 'media'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# ✅ CORRECTION 2 : Static files bien configurés
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' # Dossier pour la production

# Utiliser whitenoise pour compresser les fichiers statiques
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ✅ CORRECTION 3 : Media files (documents uploadés)
MEDIA_URL = '/media/'
# MEDIA_ROOT est déjà défini dynamiquement ci-dessus
# MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Redirections après connexion/déconnexion
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Mapping des tags Django → classes Bootstrap
from django.contrib.messages import constants as messages_constants
MESSAGE_TAGS = {
    messages_constants.DEBUG:   'info',
    messages_constants.INFO:    'info',
    messages_constants.SUCCESS: 'success',
    messages_constants.WARNING: 'warning',
    messages_constants.ERROR:   'error',  # géré manuellement dans base.html
}

# Permet l'affichage des PDF dans les iframes (même origine)
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Taille max de fichier uploadé : 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# Évite certains blocages de connexion sur localhost
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

