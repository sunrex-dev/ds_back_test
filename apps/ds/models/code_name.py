from django.db import models
from django.contrib import admin
from apps.tenants.models import *

class Code_Name(TenantBaseModel):
    """
コード名称のマスタテーブル
[更新説明]
・管理者用画面にて追加・修正・削除を行う。
    """
    class Meta:
        db_table = 'ds_code_name'
        verbose_name_plural = 'コード名称（ds_code_name）'
        unique_together = ('tenant', 'code', 'item_id')

    ITEMTYPE_LIST = ((1, '文字'), (2, '数字'))
    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    code = models.CharField(verbose_name='コード', max_length=20)
    name = models.CharField(verbose_name='コード名称', max_length=200, blank=True, null=True)
    item_id = models.IntegerField(verbose_name='項目ID')
    item_name = models.CharField(verbose_name='項目名称', max_length=200, blank=True, null=True)
    item_type = models.SmallIntegerField(verbose_name='項目タイプ', choices=ITEMTYPE_LIST)
    item_val = models.TextField(verbose_name='項目値', blank=True, null=True)
    item_val2 = models.TextField(verbose_name='項目値その2', blank=True, null=True)
    item_val3 = models.TextField(verbose_name='項目値その3', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='有効', default=True)

    def __str__(self):
        return 'ID:{0},CODE:{1},name:{2},ITEM_ID:{3},ITEM_NAME:{3}' \
        .format(self.id, self.code, self.name, self.item_id, self.item_name)

# 管理者用画面での編集内容
class Code_Name_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'code', 'name', 'item_id', 'item_name', 'is_active', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', 'code', 'is_active')
    search_fields = ('code', 'name', 'item_name', 'rulebook_comment')

# 管理者画面に表示
admin.site.register(Code_Name, Code_Name_Admin)
