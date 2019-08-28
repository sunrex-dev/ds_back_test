from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from apps.users.models import User

class Rulebook(TenantBaseModel):
    """
ルールブックのテーブル
[更新説明]
・ルールブック画面での随時更新
・更新時は、idをキーにしてUpdateを行う。
    """
    class Meta:
        db_table = 'ds_rulebook'
        verbose_name_plural = 'ルールブック（ds_rulebook）'
        unique_together = ('tenant', 'name', 'ruletype')

    RULETYPE_LIST = ((1, 'アドバイス'), (2, 'アラート'))
    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    name = models.CharField(verbose_name='ルール名', max_length=200, blank=True, null=True)
    ruletype = models.SmallIntegerField(verbose_name='ルールタイプ', choices=RULETYPE_LIST)
    comment = models.TextField(verbose_name='アドバイス（アラート）')
    rank = models.SmallIntegerField(verbose_name='ルール重要度')
    is_active = models.BooleanField(verbose_name='有効', default=True)
    update_user = models.ForeignKey(User, verbose_name='更新ユーザー管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    update_user_name = models.CharField(verbose_name='更新ユーザー名', max_length=100, blank=True, null=True)
    condition_where = models.TextField(verbose_name='条件内容', blank=True, null=True)

    def __str__(self):
        return 'ID:{0},NAME:{1},RULETYPE:{2},COMMENT:{3}' \
        .format(self.id, self.name, self.ruletype, self.comment)

# 管理者用画面での編集内容
class Rulebook_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'name', 'ruletype', 'rank', 'is_active', 'comment', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', 'ruletype', 'rank', 'is_active')
    search_fields = ('name', 'comment', 'condition_where')

# 管理者画面に表示
admin.site.register(Rulebook, Rulebook_Admin)
