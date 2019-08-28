from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.customer import *
from ..models.anken import *
from ..models.rulebook import *

class Anken_Advice(TenantBaseModel):
    """
アドバイス（アラート）のテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_anken, ds_history, ds_customer, ds_rulebook etc より取得したデータを基にして更新する。
（ds_anken.result='継続'に紐づくanken_id or ds_history.anken_id=Nullに紐づくcustomer_idが対象）
・全データを対象として、Delete + Insert を行う。
    """
    class Meta:
        db_table = 'ds_anken_advice'
        verbose_name_plural = 'アドバイス（アラート）（ds_anken_advice）'
        unique_together = ('tenant', 'customer', 'anken', 'rulebook')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    customer = models.ForeignKey(Customer, verbose_name='顧客管理ID', on_delete=models.CASCADE)
    customer_name = models.CharField(verbose_name='顧客名', max_length=200, blank=True, null=True)
    anken = models.ForeignKey(Anken, verbose_name='商談案件管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    anken_name = models.CharField(verbose_name='商談案件名', max_length=200, blank=True, null=True)
    last_visit_dt = models.DateTimeField(verbose_name='最終訪問日時', blank=True, null=True)
    rulebook = models.ForeignKey(Rulebook, verbose_name='ルールブック管理ID', on_delete=models.DO_NOTHING)
    rulebook_ruletype = models.SmallIntegerField(verbose_name='ルールタイプ')
    rulebook_name = models.CharField(verbose_name='ルール名', max_length=200, blank=True, null=True)
    rulebook_comment = models.TextField(verbose_name='アドバイス（アラート）')
    rulebook_rank = models.SmallIntegerField(verbose_name='ルール重要度')

    def __str__(self):
        return 'ID:{0},CUSTOMER_NAME:{1},ANKEN_NAME:{2},RULEBOOK_NAME:{3}' \
        .format(self.id, self.customer_name, self.anken_name, self.rulebook_name)

# 管理者用画面での編集内容
class Anken_Advice_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'customer_name', 'anken_name', 'last_visit_dt', 'rulebook_name', 'rulebook_comment', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', 'rulebook_ruletype', 'rulebook_rank')
    search_fields = ('customer_name', 'anken_name', 'rulebook_name', 'rulebook_comment')

# 管理者画面に表示
admin.site.register(Anken_Advice, Anken_Advice_Admin)
