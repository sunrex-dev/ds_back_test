# 開発環境用設定
from .base import *
import environ

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '8w#i@ct+!@ovrfs6a&3eno)_wsnh=h!)dx6y$s-i(w7#rvvy53'
#envファイルが存在したら設定を読み込む（ただし同じ変数の値は上書きされない）
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env.local'))
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ROOT_URLCONF = 'config.urls.local'

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

MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'media_root')
MEDIA_URL = '/media/'

# 静的ファイルの配信元
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'static_root')
# 静的ファイル配信⽤のディレクトリで、URLの⼀ 部になる。
STATIC_URL = '/static/'

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
        # 開発用
        'local': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s'
        },
        # Back Graund Job用
        'bgformat': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    # ハンドラ
    'handlers': {
        # コンソール出力用ハンドラ
        'console': {
            #ログレベル「CRITICAL」「ERROR」「WARNING」「INFO」「DEBUG」
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'local',
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
        #    'handlers': ['console'],
        #    'level': 'INFO',
        #    'propagate': False,
        #},
        # Django 本体が出すログ全般を拾うロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # 発行されるSQL文を出力するための設定
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Back Graund Jobのログを拾うロガー
        'bgjob': {
            'handlers': ['console','bgfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# MODELSDOC
INSTALLED_APPS += ['modelsdoc',]
MODELSDOC_APPS = ('users','tenants','ds','dblogs')
MODELSDOC_DISPLAY_FIELDS = (
    ('Fullname', 'verbose_name'),
    ('Name', 'name'),
    ('Type', 'db_type'),
    ('PK', 'primary_key'),
    ('Unique', 'unique'),
    ('Index', 'db_index'),
    ('Null/Blank', 'null_blank'),
    ('Comment', 'comment'),
)
MODELSDOC_MODEL_OPTIONS = (
    'unique_together',
    'index_together',
    'ordering',
    'permissions',
    'get_latest_by',
    'order_with_respect_to',
    'db_tablespace',
    'abstract',
    'swappable',
    'select_on_save',
    'default_permissions',
    'default_related_name'
)
MODELSDOC_OUTPUT_TEMPLATE = 'modelsdoc/models'
MODELSDOC_OUTPUT_FORMAT = 'md' # default format rst or md
MODELSDOC_MODEL_WRAPPER = 'modelsdoc.wrappers.ModelWrapper'
MODELSDOC_FIELD_WRAPPER = 'modelsdoc.wrappers.FieldWrapper'
MODELSDOC_INCLUDE_AUTO_CREATED = False

# django-debug-toolbar
def show_toolbar(request):
    return True

INSTALLED_APPS += (
    'debug_toolbar',
)
MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
# ここで表示する内容を設定
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

#DEBUG_TOOLBAR_PANELS = [
#    'debug_toolbar.panels.versions.VersionsPanel',
#    'debug_toolbar.panels.timer.TimerPanel',
#    'debug_toolbar.panels.settings.SettingsPanel',
#    'debug_toolbar.panels.headers.HeadersPanel',
#    'debug_toolbar.panels.request.RequestPanel',
#    'debug_toolbar.panels.sql.SQLPanel',
#    'debug_toolbar.panels.templates.TemplatesPanel',
#    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#    'debug_toolbar.panels.cache.CachePanel',
#    'debug_toolbar.panels.signals.SignalsPanel',
#    'debug_toolbar.panels.logging.LoggingPanel',
#    'debug_toolbar.panels.redirects.RedirectsPanel',
#    'debug_toolbar.panels.profiling.ProfilingPanel',
#]

#INTERNAL_IPS = ['127.0.0.1']
