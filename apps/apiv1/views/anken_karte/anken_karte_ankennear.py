from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.anken_near import Anken_Near

class AnkenKarteAnkNearListSerial(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', help_text='顧客名')
    anken_near_name = serializers.CharField(source='anken.name', help_text='類似案件名')

    class Meta:
        model=Anken_Near
        fields = ('id', 'anken_result_kbn', 'customer_name', 'anken_near_name', 'near_rate')

class AnkenKarteAnkNearListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteAnkNearListSerial
    ordering_fields = ('anken_result_kbn','near_rate',)
    ordering = ('anken_result_kbn','-near_rate')

    def get_queryset(self):
        query = Anken_Near.objects.get_queryset().filter(customer_id=self.kwargs['customer_id']) 
        if self.kwargs['anken_id'] != 0:
            query = query.filter(anken_id=self.kwargs['anken_id'])
        return query

    @swagger_auto_schema(operation_summary="[案件カルテ]の[類似案件一覧]取得", manual_parameters=[
        openapi.Parameter('customer_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の顧客データを識別する一意の整数値'),
        openapi.Parameter('anken_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の案件データを識別する一意の整数値（未指定時は0をセット）'),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[類似案件一覧]取得
        """
        return super().get(request, *args, **kwargs)
