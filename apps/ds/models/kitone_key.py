from django.db import models
from django.contrib import admin
from apps.tenants.models import *

class Kintone_Key(TenantBaseModel):
    """
Kintoneへのアクセス情報の管理テーブル
[更新説明]
・必要に応じて随時、admin管理画面より追加/修正/削除を行う。
    """
    class Meta:
        db_table = 'ds_kintone_key'
        verbose_name_plural = 'kintone API KEY 設定（ds_kintone_key）'
        unique_together = ('tenant', 'app_id')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    name = models.CharField(verbose_name='名前', max_length=100)
    domain = models.CharField(verbose_name='DOMAIN', max_length=100)
    app_id = models.CharField(verbose_name='APP ID', max_length=100)
    api_token = models.CharField(verbose_name='API TOKEN', max_length=100)
    deleted = models.BooleanField(verbose_name='削除フラグ', default=False)

    def __str__(self):
        return 'ID:{0},DOMAIN:{1},APP_ID:{2},DELETED:{3}' \
        .format(self.id, self.domain, self.app_id, self.deleted)

# 管理者用画面での編集内容
class Kintone_Key_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'name', 'domain', 'app_id', 'deleted', 'created_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', 'deleted')
    search_fields = ('name', 'domain')

# 管理者画面に表示
admin.site.register(Kintone_Key, Kintone_Key_Admin)
