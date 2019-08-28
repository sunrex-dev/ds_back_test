from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.anken_successrt_cmt import Anken_Successrt_Cmt

class AnkenKarteSucsCmtSerial(serializers.ModelSerializer):
    class Meta:
        model=Anken_Successrt_Cmt
        fields = ('id', 'customer_id', 'anken_id', 'comment', 'successup_rate')

class AnkenKarteSucsCmtListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteSucsCmtSerial
    lookup_field = 'anken_id'
    ordering_fields = ('successup_rate',)
    ordering = ('-successup_rate')

    def get_queryset(self):
        return Anken_Successrt_Cmt.objects.get_queryset()

    @swagger_auto_schema(operation_summary="[案件カルテ]の[案件分析コメント]取得", manual_parameters=[
        openapi.Parameter('anken_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の案件データを識別する一意の整数値'),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[案件分析コメント]取得
        """
        return super().get(request, *args, **kwargs)
