from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.customer import *
from ..models.anken import *

class Anken_Near(TenantBaseModel):
    """
類似案件のテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_history, ds_anken, ds_customer より取得したデータを基にして更新する。
（ds_history.updated_atが本日であるデータに紐づくcustomer_id, anken_idが対象）
・customer_idとanken_idが同じであるデータが存在した場合は、Delete + Insertを行う。
（anken_idがNullの場合（未案件分）は、anken_id=Nullを条件とする。）
    """
    class Meta:
        db_table = 'ds_anken_near'
        verbose_name_plural = '類似案件（ds_anken_near）'
        unique_together = ('tenant', 'customer', 'anken', 'anken_near' )

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    customer = models.ForeignKey(Customer, verbose_name='顧客管理ID', on_delete=models.CASCADE)
    customer_name = models.CharField(verbose_name='顧客名', max_length=200, blank=True, null=True)
    anken = models.ForeignKey(Anken, verbose_name='商談案件管理ID', null=True, on_delete=models.DO_NOTHING, related_name='anken', db_constraint=False)
    anken_name = models.CharField(verbose_name='商談案件名', max_length=200, blank=True, null=True)
    anken_near = models.ForeignKey(Anken, verbose_name='商談案件管理ID（類似）', related_name='anken_near', on_delete=models.DO_NOTHING)
    anken_near_name = models.CharField(verbose_name='商談案件名（類似）', max_length=200, blank=True, null=True)
    anken_result = models.CharField(verbose_name='結果', max_length=20, blank=True, null=True)
    near_rate = models.FloatField(verbose_name='類似率')
    anken_result_kbn = models.SmallIntegerField(verbose_name='結果区分',help_text='2:成約,3:敗戦',default=0)

    def __str__(self):
        return 'ID:{0},ANKEN_ID:{1},ANKEN_NAME:{2}' \
        .format(self.id, self.anken_id, self.anken_name)

# 管理者用画面での編集内容
class Anken_Near_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'customer_name', 'anken_name', 'anken_near_name', 'anken_result', 'near_rate', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', )
    search_fields = ('customer_name', 'anken_name', 'anken_near_name', 'anken_result')

# 管理者画面に表示
admin.site.register(Anken_Near, Anken_Near_Admin)
