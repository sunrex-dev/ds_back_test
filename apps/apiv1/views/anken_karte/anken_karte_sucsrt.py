from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.anken_successrt import Anken_Successrt

class AnkenKarteSucsrtSerial(serializers.ModelSerializer):
    class Meta:
        model=Anken_Successrt
        fields = ('id', 'customer_id', 'anken_id', 'success_rate')

class AnkenKarteSucsrtView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteSucsrtSerial
    lookup_field = 'anken_id'

    def get_queryset(self):
        return Anken_Successrt.objects.get_queryset()

    @swagger_auto_schema(operation_summary="[案件カルテ]の[案件分析成約確率]取得", manual_parameters=[
        openapi.Parameter('anken_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の案件データを識別する一意の整数値'),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[案件分析成約確率]取得
        """
        return super().get(request, *args, **kwargs)
