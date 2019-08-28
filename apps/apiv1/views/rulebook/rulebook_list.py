from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.ds.models.rulebook import Rulebook

class RulebookListSerial(serializers.ModelSerializer):
    class Meta:
        model=Rulebook
        fields = ('id', 'ruletype', 'name', 'comment', 'rank', 'updated_at')

class RulebookListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RulebookListSerial
    ordering_fields = ('ruletype','name','comment','rank', 'updated_at')
    ordering = ('ruletype','-updated_at')
    filter_fields = ('ruletype', 'is_active',)
    search_fields = ('name','comment','condition_where')

    def get_queryset(self):
        query = Rulebook.objects.get_queryset() 
        return query

    @swagger_auto_schema(operation_summary="[ルールブック]の[一覧]取得", manual_parameters=[
        openapi.Parameter('ruletype', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ルールタイプを指定（1:アドバイス,2:アラート）'),
        openapi.Parameter('is_active', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='有効状態を指定（true:有効,false:無効）'),
        openapi.Parameter('search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='対象項目に対する検索キーワードを指定　'+str(search_fields)),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [ルールブック]の[一覧]取得
        """
        return super().get(request, *args, **kwargs)
