# 開発環境用設定
from django.urls import path, include

urlpatterns = [
    # URLの読み込み
    path('api-products/salesapi_rc/', include('config.urls.base')),
    path('api-products/salesapi_rc/', include('config.urls.swagger.local')),
]

# debug_toolbar 設定
import debug_toolbar
urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
]
