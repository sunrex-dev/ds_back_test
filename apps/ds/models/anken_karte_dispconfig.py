from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from apps.users.models import User

class Anken_Karte_DispConfig(TenantBaseModel):
    """
案件カルテ表示設定のテーブル
[更新説明]
・案件カルテ画面で、各カードの位置情報を変更した際に更新する。
・user_idでDeleteした後、Insertを行う。
    """
    class Meta:
        db_table = 'ds_anken_karte_dispconfig'
        verbose_name_plural = '案件カルテ表示設定（ds_anken_karte_dispconfig）'
        unique_together = ('tenant', 'user', 'dispno')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    user = models.ForeignKey(User, verbose_name='ユーザー管理ID', null=True, on_delete=models.CASCADE)
    user_name = models.CharField(verbose_name='ユーザー名', max_length=100, blank=True, null=True)
    dispno = models.SmallIntegerField(verbose_name='表示No')
    item_id = models.IntegerField(verbose_name='項目ID')
    item_name = models.CharField(verbose_name='項目名称', max_length=200, blank=True, null=True)

    def __str__(self):
        return 'ID:{0},USER_NAME:{1},DISPNO:{2},ITEM_ID:{3},ITEM_NAME:{3}' \
        .format(self.id, self.user_name, self.dispno, self.item_id, self.item_name)

# 管理者用画面での編集内容
class Anken_Karte_DispConfig_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'user_name', 'dispno', 'item_id', 'item_name', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id',)
    search_fields = ('user_name', 'item_name')

# 管理者画面に表示
admin.site.register(Anken_Karte_DispConfig, Anken_Karte_DispConfig_Admin)
