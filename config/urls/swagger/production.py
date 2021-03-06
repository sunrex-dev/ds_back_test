# swagger 追記(drf-yasg)
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required

schema_view = get_schema_view(
   openapi.Info(
      title="DeepSales API",
      default_version='v1',
      #description="Test description",
      #terms_of_service="https://www.google.com/policies/terms/",
      #contact=openapi.Contact(email="contact@snippets.local"),
      #license=openapi.License(name="BSD License"),
   ),
   url='https://demo.sunrex.co.jp/api-products/salesapi_rc/',
   public=True,
   permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
   url(r'swagger(?P<format>\.json|\.yaml)$', login_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
   url(r'swagger/$', login_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
   url(r'redoc/$', login_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
   path('auth/', include('rest_framework.urls', namespace='rest_framework')),
 
]
