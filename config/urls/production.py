# 本番環境用設定
from django.urls import path, include

urlpatterns = [
    # URLの読み込み
    path('api-products/salesapi_rc/', include('config.urls.base')),
]
