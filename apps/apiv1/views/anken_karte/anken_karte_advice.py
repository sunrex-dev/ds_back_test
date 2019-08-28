from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.anken_advice import Anken_Advice

class AnkenKarteAdviceSerial(serializers.ModelSerializer):
    class Meta:
        model=Anken_Advice
        fields = ('id', 'customer_id', 'anken_id', 'rulebook_comment', 'rulebook_rank', 'last_visit_dt')

class AnkenKarteAdviceListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteAdviceSerial
    ordering_fields = ('rulebook_rank','last_visit_dt',)
    ordering = ('-rulebook_rank','-last_visit_dt')

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Anken_Advice.objects.none()
        query = Anken_Advice.objects.get_queryset() 
        query = query.filter(rulebook_ruletype=1)
        query = query.filter(customer_id=self.kwargs['customer_id'])
        if self.kwargs['anken_id'] != 0:
            query = query.filter(anken_id=self.kwargs['anken_id'])
        return query

    @swagger_auto_schema(operation_summary="[案件カルテ]の[アドバイス]取得", manual_parameters=[
        openapi.Parameter('customer_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の顧客データを識別する一意の整数値'),
        openapi.Parameter('anken_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の案件データを識別する一意の整数値（未指定時は0をセット）'),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[アドバイス]取得
        """
        return super().get(request, *args, **kwargs)
