from django.db.models import *
from django.db.models.functions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.anken import Anken

class AnkenKarteAnkeninfoSerial(serializers.ModelSerializer):
    close_plan_rank = serializers.SerializerMethodField()
    visit_count = serializers.IntegerField()
    visit_times_sum = serializers.IntegerField()

    class Meta:
        model=Anken
        fields = ('id', 'no', 'name', 'close_plan_total', 'close_plan_rank',  \
                  'employee_name', 'customer_person', 'visit_count', 'visit_times_sum')
    
    def get_close_plan_rank(self, instance):
        if instance.close_plan_total >= 10000000:
            return 'A'
        elif instance.close_plan_total >= 1000000 and instance.close_plan_total <= 9999999:
            return 'B'
        elif instance.close_plan_total >= 100000 and instance.close_plan_total <= 999999:
            return 'C'
        else:
            return 'D'

class AnkenKarteAnkeninfoView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnkenKarteAnkeninfoSerial
    #lookup_field = 'no'

    def get_queryset(self):
        query = Anken.objects
        query = query.annotate(
            visit_count=Count('history__id'),
            visit_times_sum=Coalesce(Sum('history__visit_times'),0))
        #print(query.query)
        return query

    @swagger_auto_schema(operation_summary="[案件カルテ]の[案件情報]取得", manual_parameters=[
        openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定の案件データを識別する一意の整数値'),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [案件カルテ]の[案件情報]取得
        """
        return super().get(request, *args, **kwargs)
