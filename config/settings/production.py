# 本番環境用設定
from .base import *
import environ

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'p@02z4ve40&#vyx^#n2@5cuqol*lq=9$c3)xmqwi0%5cyv6xbe'
#envファイルが存在したら設定を読み込む（ただし同じ変数の値は上書きされない）
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env.production'))
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ROOT_URLCONF = 'config.urls.production'

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'TRADITIONAL',
        },
    },
}

# Static files (CSS, JavaScript, Images)

MEDIA_ROOT = '/var/www/{}/media'.format(PROJECT_NAME)
MEDIA_URL = '/media/'

STATIC_ROOT = '/var/www/{}/static'.format(PROJECT_NAME)
STATIC_URL = '/api-products/api-static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

LOGGING = {
    # バージョンは「1」固定
    'version': 1,
    # 既存のログ設定を無効化しない
    'disable_existing_loggers': False,
    # ログフォーマット
    'formatters': {
        # 本番用
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s'
        },
        # Back Graund Job用
        'bgformat': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    # ハンドラ
    'handlers': {
        # ファイル出力用ハンドラ
        'file': {
            'level': 'INFO',
            'filename': 'logs/django.log',  #環境に合わせて変更
            'formatter': 'production',
            #'class': 'logging.handlers.RotatingFileHandler',
            #'maxBytes': 50000,
            #'backupCount': 3, # 世代数
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D', # 単位は日
            'interval': 3, # 3日おき
            'backupCount': 10, # 世代数
        },
        # Back Graund Job用
        'bgfile': {
            'level': 'DEBUG',
            'filename': BASE_DIR + '/logs/bgjob.log',  #環境に合わせて変更
            'formatter': 'bgformat',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*50, # 50 MB
            'backupCount': 3, # 世代数
        },
    },
    # ロガー
    'loggers': {
        ## 自作アプリケーション全般のログを拾うロガー
        #'': {
        #    'handlers': ['file'],
        #    'level': 'INFO',
        #    'propagate': False,
        #},
        # Django 本体が出すログ全般を拾うロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        # 発行されるSQL文を出力するための設定
        #'django.db.backends': {
        #    'handlers': ['file'],
        #    'level': 'DEBUG',
        #    'propagate': False,
        #},
        # Back Graund Jobのログを拾うロガー
        'bgjob': {
            'handlers': ['bgfile'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
