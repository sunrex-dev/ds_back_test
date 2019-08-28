from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
#from django.db.models.functions import Concat
from django.db.models import Max
from apps.ds.models.dictionary import Dictionary
from django_mysql.models import GroupConcat

class DictionaryListSerial(serializers.ModelSerializer):
    distword_list = serializers.ReadOnlyField(help_text='キーワードリスト')
    last_updated_at = serializers.ReadOnlyField(help_text='最終更新日')
    
    class Meta:
        model=Dictionary
        fields = ('typekbn', 'grpname', 'distword_list', 'last_updated_at')

class DictionaryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DictionaryListSerial
    ordering_fields = ('typekbn','grpname', 'last_updated_at')
    ordering = ('typekbn','grpname')
    filter_fields = ('typekbn', 'is_active',)
    search_fields = ('grpname', 'distword_list')

    def get_queryset(self):
        query = Dictionary.objects.get_queryset() 
        query = query.values('typekbn', 'grpname')
        query = query.annotate(distword_list=GroupConcat('distword'))
        query = query.annotate(last_updated_at=Max('updated_at'))
        return query

    @swagger_auto_schema(operation_summary="[辞書]の[一覧]取得", manual_parameters=[
        openapi.Parameter('typekbn', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='キーワードタイプを指定（1:単語@,2:振る舞い#）'),
        openapi.Parameter('is_active', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description='有効状態を指定（true:有効,false:無効）'),
        openapi.Parameter('search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='対象項目に対する検索キーワードを指定　'+str(search_fields)),
        openapi.Parameter('ordering', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='取得時のソート対象となる項目を指定　'+str(ordering_fields)),
    ],responses={'401': openapi.Response(description='認証失敗',)})
    def get(self, request, *args, **kwargs):
        """
        [辞書]の[一覧]取得
        """
        return super().get(request, *args, **kwargs)
