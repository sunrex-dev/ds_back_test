from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.customer import Customer

class AnkenKarteCustomerSerial(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model=Customer
        fields = ('id', 'no', 'name', 'address', 'tel', 'yealy_sales', 'employee_number',  \
                  'products', 'industry_type', 'hp_url')
    
    def get_address(self, instance):
        return '{0} {1}'.format(instance.prefecture_name, instance.city_name).strip()

class AnkenKarteCustomerView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteCustomerSerial
    #lookup_field = 'no'
    
    def get_queryset(self):
        return Customer.objects.get_queryset()

    @swagger_auto_schema(operation_summary="[案件カルテ]の[顧客情報]取得", manual_parameters=[
        openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の顧客データを識別する一意の整数値'),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[顧客情報]取得
        """
        return super().get(request, *args, **kwargs)
