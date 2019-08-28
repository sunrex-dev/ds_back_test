from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView

# 追加
admin.site.site_title = 'DeepSales 管理サイト' 
admin.site.site_header = 'DeepSales 管理サイト' 
admin.site.index_title = 'メニュー'

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # top
    path('', TemplateView.as_view(template_name='index.html')),

    # v1
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/ds/', include('apps.apiv1.urls')),

]

# 該当しないURLの場合
#urlpatterns += [
#    re_path('', RedirectView.as_view(url='/api/')),
#]
