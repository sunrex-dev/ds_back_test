from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from apps.users.models import User

class Dictionary(TenantBaseModel):
    """
辞書のテーブル
[更新説明]
・辞書管理画面での随時更新、又は1回/日の間隔にて学習用の更新を行う。
・更新時は、idをキーにしてUpdateを行う。
    """
    class Meta:
        db_table = 'ds_dictionary'
        verbose_name_plural = '辞書（ds_dictionary）'
        unique_together = ('tenant', 'grpname', 'typekbn', 'distword')

    TYPEKBN_LIST = ((1, '単語@'), (2, '振る舞い#'))
    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    grpname = models.CharField(verbose_name='辞書グループ名', max_length=200)
    typekbn = models.SmallIntegerField(verbose_name='辞書タイプ', choices=TYPEKBN_LIST)
    distword = models.CharField(verbose_name='辞書キーワード', max_length=200)
    point = models.SmallIntegerField(verbose_name='辞書ポイント')
    is_perfect_match = models.BooleanField(verbose_name='全一致区分')
    is_learned = models.BooleanField(verbose_name='学習済区分')
    learned_at = models.DateTimeField(verbose_name='学習日時', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='有効', default=True)
    update_user = models.ForeignKey(User, verbose_name='更新ユーザー管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    update_user_name = models.CharField(verbose_name='更新ユーザー名', max_length=100, blank=True, null=True)

    def __str__(self):
        return 'ID:{0},GRPNAME_NAME:{1},TYPEKBN:{2},DISTWORD:{3}' \
        .format(self.id, self.grpname, self.typekbn, self.distword)
    
# 管理者用画面での編集内容
class Dictionary_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'grpname', 'typekbn', 'distword', 'point', 'is_perfect_match', 'is_learned', 'is_active', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', 'typekbn', 'is_perfect_match', 'is_learned', 'is_active')
    search_fields = ('grpname', 'distword')

# 管理者画面に表示
admin.site.register(Dictionary, Dictionary_Admin)
