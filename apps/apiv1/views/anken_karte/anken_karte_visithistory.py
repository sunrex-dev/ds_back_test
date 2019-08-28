from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.history import History

class AnkenKarteVisHisListSerial(serializers.ModelSerializer):
    class Meta:
        model=History
        fields = ('id', 'no', 'visit_dt', 'employee_name', 'purpose', 'result',  \
                  'customer_id', 'anken_id',)

class AnkenKarteVisHisListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteVisHisListSerial
    filter_fields = ('customer_id', 'anken_id',)
    ordering_fields = ('visit_dt', 'employee_name', 'result',)
    ordering = ('-visit_dt')

    def get_queryset(self):
        return History.objects.get_queryset()

    @swagger_auto_schema(operation_summary="[案件カルテ]の[訪問履歴一覧]取得", manual_parameters=[
        openapi.Parameter('customer_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='特定の顧客データを識別する一意の整数値'),
        openapi.Parameter('anken_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='特定の案件データを識別する一意の整数値'),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[訪問履歴一覧]取得
        """
        return super().get(request, *args, **kwargs)

class AnkenKarteVisHisDetailSerial(serializers.ModelSerializer):
    class Meta:
        model=History
        fields = '__all__'

class AnkenKarteVisHisDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteVisHisDetailSerial
    #lookup_field = 'no'

    def get_queryset(self):
        return History.objects.get_queryset()

    @swagger_auto_schema(operation_summary="[案件カルテ]の[訪問履歴詳細]取得", manual_parameters=[
        openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の案件データを識別する一意の整数値'),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[訪問履歴詳細]取得
        """
        return super().get(request, *args, **kwargs)
