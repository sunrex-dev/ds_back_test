from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.history import *
from ..models.customer import *
from ..models.anken import *
from ..models.dictionary import *

class Keyword(TenantBaseModel):
    """
キーワードのテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_history, ds_dictonary より取得したデータを基にして更新する。
（ds_history.updated_atが本日であるデータが対象）
・history_idが同じであるデータが存在した場合は, 最初にhistory_id単位でDeleteし、
 その後Insert時に、history_id + dictionary_idが同じデータが既存する場合はスキップする。
    """
    class Meta:
        db_table = 'ds_keyword'
        verbose_name_plural = 'アドバイス（アラート）（ds_keyword）'
        unique_together = ('tenant', 'history', 'dictionary')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    history = models.ForeignKey(History, verbose_name='商談履歴管理ID', on_delete=models.CASCADE)
    history_result = models.TextField(verbose_name='面談結果', max_length=10000, blank=True, null=True)
    history_visit_dt = models.DateTimeField(verbose_name='実訪問日時', blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name='顧客管理ID', on_delete=models.CASCADE)
    customer_name = models.CharField(verbose_name='顧客名', max_length=200, blank=True, null=True)
    anken = models.ForeignKey(Anken, verbose_name='商談案件管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    anken_name = models.CharField(verbose_name='商談案件名', max_length=200, blank=True, null=True)
    dictionary = models.ForeignKey(Dictionary, verbose_name='辞書管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    dictionary_grpname = models.CharField(verbose_name='辞書グループ名', max_length=200)
    dictionary_typekbn = models.SmallIntegerField(verbose_name='辞書タイプ')
    dictionary_distword = models.CharField(verbose_name='辞書キーワード', max_length=200)
    dictionary_point = models.SmallIntegerField(verbose_name='辞書ポイント')

    def __str__(self):
        return 'ID:{0},CUSTOMER_NAME:{1},ANKEN_NAME:{2},HISTORY_ID:{3}' \
        .format(self.id, self.customer_name, self.anken_name, self.history_id)

# 管理者用画面での編集内容
class Keyword_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'history_id', 'history_visit_dt', 'customer_name', 'anken_name', 'dictionary_grpname', 'dictionary_typekbn', 'dictionary_distword', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', 'dictionary_typekbn')
    search_fields = ('customer_name', 'anken_name', 'dictionary_grpname', 'dictionary_distword')

# 管理者画面に表示
admin.site.register(Keyword, Keyword_Admin)
