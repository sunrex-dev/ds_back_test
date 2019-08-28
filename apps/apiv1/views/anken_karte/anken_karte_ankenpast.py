from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.anken import Anken

class AnkenKarteAnkPastListSerial(serializers.ModelSerializer):
    class Meta:
        model=Anken
        fields = ('id', 'no', 'result', 'name', 'employee_name', 'close_dt',  \
                  'customer_id', 'customer_name')

class AnkenKarteAnkPastListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteAnkPastListSerial
    #lookup_field = 'customer_id'
    filter_fields = {'close_dt':['exact', 'gte', 'lte'],}
    ordering_fields = ('close_dt', 'name', 'employee_name', 'result',)
    ordering = ('-close_dt')

    def get_queryset(self):
        query = Anken.objects.get_queryset().filter(customer_id=self.kwargs['customer_id']) 
        query = query.filter(result__in=['成約','敗戦'])
        return query

    @swagger_auto_schema(operation_summary="[案件カルテ]の[過去案件一覧]取得", manual_parameters=[
        openapi.Parameter('customer_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の顧客データを識別する一意の整数値'),
        openapi.Parameter('close_dt', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='成約日を日付指定（yyyy-MM-dd）(以上:__gteを付加,以下:__lteを付加)'),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[過去案件一覧]取得
        """
        return super().get(request, *args, **kwargs)
