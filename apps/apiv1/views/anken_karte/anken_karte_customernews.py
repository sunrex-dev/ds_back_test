from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.customer_news import Customer_News

class AnkenKarteCustNewsSerial(serializers.ModelSerializer):
    class Meta:
        model=Customer_News
        fields = ('id', 'customer_id', 'news_no', 'news_title', 'news_url')

class AnkenKarteCustNewsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteCustNewsSerial
    lookup_field = 'customer_id'
    ordering_fields = ('news_no', 'updated_at')
    ordering = ('-updated_at')

    def get_queryset(self):
        query = Customer_News.objects.get_queryset()
        query = query.filter(news_no__gle=1)
        return query

    @swagger_auto_schema(operation_summary="[案件カルテ]の[顧客ニュース]取得", manual_parameters=[
        openapi.Parameter('customer_id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の顧客データを識別する一意の整数値'),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[顧客ニュース]取得
        """
        return super().get(request, *args, **kwargs)
