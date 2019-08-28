# 基本設定（本番環境、開発環境　共通）
import os, sys
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_NAME = os.path.basename(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '8w#i@ct+!@ovrfs6a&3eno)_wsnh=h!)dx6y$s-i(w7#rvvy53' → 個別設定へ移行

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True → 個別設定へ移行

# ALLOWED_HOSTS = [] → 個別設定へ移行

# Add apps/ to the Python path
#sys.path.append(os.path.join(BASE_DIR, "apps"))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'rest_framework',
    #'rest_framework_swagger',
    'drf_yasg',
    'django_filters',
    'corsheaders',
    'djoser',
    'sequences.apps.SequencesConfig',
    'django_extensions',

    # My applications
    'apps.users',
    'apps.tenants',
    'apps.dblogs',
    'apps.ds',
    'apps.apiv1',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 3rd party middleware
    'corsheaders.middleware.CorsMiddleware',
    
    # My applications
    'apps.tenants.middleware.SetCurrentTenantFromUser',
    'apps.dblogs.middleware.AccessLogsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# 個別設定へ移行
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Authentication
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'
LOGIN_REDIRECT_URL = '/' # 追加
# LOGOUT_REDIRECT_URL = 'rest_framework:login' # 追加
AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
        #'apps.apiv1.filters.custom_backend.CustomDjangoFilterBackend',
    ),
    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    #'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    #'SEARCH_PARAM': 'q',
    # Parser classes priority-wise for Swagger
    'EXCEPTION_HANDLER': 'apps.apiv1.utils.handler.custom_exception_handler',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    #'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_URL = '/static/' → 個別設定へ移行

# CORS
CORS_ORIGIN_ALLOW_ALL = True

# swagger
# 認証ありのAPIもSwaggerUIから使えるように、`LOGIN_URL`とか`DEFAULT_AUTHENTICATION_CLASSES`を設定
SWAGGER_SETTINGS = {
    #'LOGIN_URL': 'rest_framework:login',
    #'LOGOUT_URL': 'rest_framework:logout',
    #'PERSIST_AUTH': True,
    #'REFETCH_SCHEMA_WITH_AUTH': True,
    #'REFETCH_SCHEMA_ON_LOGOUT': True,
    'USE_SESSION_AUTH': True,
    'DOC_EXPANSION': 'none',
    'APIS_SORTER': 'alpha',
    'JSON_EDITOR': True, 
    #'SHOW_REQUEST_HEADERS': False,
    #'SUPPORTED_SUBMIT_METHODS': [
    #    'get',
    #    'post',
    #    'put',
    #    'delete',
    #    'patch'
    #],
#    'SECURITY_DEFINITIONS': {
#        'basic': {
#            'type': 'basic'
#        }
#    },
}
