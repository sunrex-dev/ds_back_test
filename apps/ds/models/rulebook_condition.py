from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.rulebook import *
from apps.users.models import User
from apps.ds.models.rulebook import Rulebook

class Rulebook_Condition(TenantBaseModel):
    """
ルールブック条件のテーブル
[更新説明]
・ルールブック画面での随時更新
・更新時は、rulebook_idをキーにしてDelete + Insertを行う。
    """
    class Meta:
        db_table = 'ds_rulebook_condition'
        verbose_name_plural = 'ルールブック条件（ds_rulebook_condition）'
        unique_together = ('tenant', 'rulebook', 'no')

    CONDITIONTYPE_LIST = ((0, '先頭条件'), (1, 'AND条件'), (2, 'OR条件'))
    ITEMTYPE_LIST = ((1, '文字'), (2, '数字'))
    CMPRTYPE_LIST=((1, '等しい'), (2, '等しくない'), (3, '以上'), (4, '以下'), (5, 'より大きい'), (6, 'より小さい'),
                   (7, '含む'), (8, '含まない'))
    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    rulebook = models.ForeignKey(Rulebook, verbose_name='ルールブック管理ID', related_name='rulecons', on_delete=models.CASCADE)
    rulebook_name = models.CharField(verbose_name='ルール名', max_length=200, blank=True, null=True)
    no = models.SmallIntegerField(verbose_name='条件No')
    conditiontype = models.SmallIntegerField(verbose_name='条件タイプ', choices=CONDITIONTYPE_LIST)
    item_id = models.IntegerField(verbose_name='項目ID')
    item_name = models.CharField(verbose_name='項目名称', max_length=200, blank=True, null=True)
    item_type = models.SmallIntegerField(verbose_name='項目タイプ', choices=ITEMTYPE_LIST)
    item_val = models.TextField(verbose_name='項目値', blank=True, null=True)
    cmpr_type = models.SmallIntegerField(verbose_name='比較タイプ',  choices=CMPRTYPE_LIST) 

    def __str__(self):
        return 'ID:{0},RULEBOOK_ID:{1},NO:{2},ITEM_NAME:{3}' \
        .format(self.id, self.rulebook_id, self.no, self.item_name)

# 管理者用画面での編集内容
class Rulebook_Condition_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'rulebook_name', 'no', 'conditiontype', 'item_name', 'item_type', 'item_val', 'cmpr_type', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', 'item_type')
    search_fields = ('rulebook_name', 'item_name', 'item_val')

# 管理者画面に表示
admin.site.register(Rulebook_Condition, Rulebook_Condition_Admin)
