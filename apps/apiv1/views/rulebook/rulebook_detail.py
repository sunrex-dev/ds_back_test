from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from sequences import get_next_value
from apps.ds.models.rulebook import Rulebook
from apps.ds.models.rulebook_condition import Rulebook_Condition

CMPR_LIST={1:'等しい', 2:'等しくない', 3:'以上', 4:'以下', 5:'より大きい', 6:'より小さい', 7:'含む', 8:'含まない'}
COND_LIST = {0:'', 1:'AND', 2:'OR'}

class RulebookConditionSerial(serializers.ModelSerializer):
    class Meta:
        model=Rulebook_Condition
        fields = ('tenant', 'rulebook_name', 'no', 'conditiontype', \
                  'item_id', 'item_name', 'item_type', 'item_val', 'cmpr_type')

class RulebookSerial(serializers.ModelSerializer):
    rulecons = RulebookConditionSerial(many=True)
    class Meta:
        model=Rulebook
        #fields = '__all__'
        fields = ('tenant', 'name', 'ruletype', 'comment', 'rank', 'is_active', \
                  'update_user', 'update_user_name', 'rulecons', 'lock_id', 'condition_where')
#        extra_kwargs = {
#                    'condition_where': {'write_only': True},
#                }
#    def validate_name(self, data):
#        qs = Rulebook.objects.filter(name=data)
#        if self.instance:
#            qs = qs.exclude(pk=self.instance.pk)
#        if qs.exists():
#            raise serializers.ValidationError("この名前は既に登録されています。")
#        return data

#    def validate(self, data):
#        #if 'python' not in data['word'] and data['parts'] != 'pythonista':
#        #    raise serializers.ValidationError("正しい内容が入力されていません")
#        return data

    def create(self, validated_data):
        rulecons_data = validated_data.pop('rulecons')
        rulebook = Rulebook.objects.create(**validated_data)
        for con_data in rulecons_data:
            Rulebook_Condition.objects.create(rulebook=rulebook, **con_data)
        return rulebook
    
    def update(self, instance, validated_data):
        rulecons_data = validated_data.pop('rulecons')
        #rulecons = instance.rulecons
        instance.name = validated_data.get('name', instance.name)
        instance.ruletype = validated_data.get('ruletype', instance.ruletype)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.update_user = validated_data.get('update_user', instance.update_user)
        instance.update_user_name = validated_data.get('update_user_name', instance.update_user_name)
        instance.lock_id = validated_data.get('lock_id', instance.lock_id)
        instance.condition_where = validated_data.get('condition_where', instance.condition_where)
        instance.save()

        Rulebook_Condition.objects.filter(rulebook=instance).delete()
        for con_data in rulecons_data:
            Rulebook_Condition.objects.create(rulebook=instance, **con_data)

        return instance

class RulebookDetaiCreatelView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RulebookSerial

#    def get_queryset(self):
#        return Rulebook.objects.get_queryset()

    @swagger_auto_schema(operation_summary="[ルールブック]の[詳細]作成", 
    responses={'400': openapi.Response(description='登録失敗',),
               '401': openapi.Response(description='認証失敗',)},
    )
    def post(self, request, *args, **kwargs):
        """
        [ルールブック]の[詳細]作成
        """
        rule_edit = Rulebook_Editor()
        resp = rule_edit.DBedit(request, None, *args, **kwargs)
        return resp

class RulebookDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RulebookSerial

    def get_queryset(self):
        return Rulebook.objects.get_queryset()

    @swagger_auto_schema(operation_summary="[ルールブック]の[詳細]取得", manual_parameters=[
        openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='特定のルールブックデータを識別する一意の整数値'),
    ],responses={'401': openapi.Response(description='認証失敗',), '404': openapi.Response(description='該当データ無し',)})
    def get(self, request, *args, **kwargs):
        """
        [ルールブック]の[詳細]取得
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="[ルールブック]の[詳細]更新", 
    responses={'400': openapi.Response(description='更新失敗',),
               '404': openapi.Response(description='該当データ無し',),
               '401': openapi.Response(description='認証失敗',)},
    )
    def put(self, request, *args, **kwargs):
        """
        [ルールブック]の[詳細]更新
        """
        instance = self.get_object()
        rule_edit = Rulebook_Editor()
        resp = rule_edit.DBedit(request, instance, *args, **kwargs)
        return resp

    @swagger_auto_schema(operation_summary="[ルールブック]の[詳細]削除", 
    responses={'400': openapi.Response(description='削除失敗',),
               '404': openapi.Response(description='該当データ無し',),
               '401': openapi.Response(description='認証失敗',)},
    )
    def delete(self, request, *args, **kwargs):
        """
        [ルールブック]の[詳細]削除
        """
        return super().delete(request, *args, **kwargs)


class Rulebook_Editor():
    """
    POST及びPUTの共通編集処理
    """
    def DBedit(self, request, instance, *args, **kwargs):
        if request.method == 'POST':
            serializer = RulebookSerial(data=request.data)
        else:
            serializer = RulebookSerial(instance, data=request.data)
            request.data['lock_id'] = get_next_value('lock_id')
        
        request.data['tenant'] = request.user.tenant_id
        request.data['update_user'] = request.user.id
        request.data['update_user_name'] = request.user.full_name

        ar_conds = []
        if 'rulecons' in request.data and type(request.data['rulecons']) == list:
            for i, tmp in enumerate(request.data['rulecons']):
                request.data['rulecons'][i]['tenant'] = request.user.tenant_id
                request.data['rulecons'][i]['no'] = i+1 
                request.data['rulecons'][i]['rulebook_name'] = request.data['name']
                ar_conds.append(
                    '{0}[項目={1},条件={2},値={3}]'.format(
                        COND_LIST.get(request.data['rulecons'][i]['conditiontype'],''),
                        request.data['rulecons'][i]['item_name'],
                        CMPR_LIST.get(request.data['rulecons'][i]['cmpr_type'],''),
                        request.data['rulecons'][i]['item_val'],
                        )
                    )

        request.data['condition_where'] = ''.join(ar_conds)

        if serializer.is_valid():
            serializer.save()
            if request.method == 'POST':
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

