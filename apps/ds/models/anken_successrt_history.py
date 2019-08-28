from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.customer import *
from ..models.anken import *

class Anken_Successrt_History(TenantBaseModel):
    """
案件成約確率履歴のテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_anken_successrt より取得したデータを基にして更新する。
・create_dtが本日であるデータを対象として、Delete + Insert を行う。（基本的にDeleteは発生しない）
    """
    class Meta:
        db_table = 'ds_anken_successrt_history'
        verbose_name_plural = '案件成約確率履歴（ds_anken_successrt_history）'
        unique_together = ('tenant', 'customer', 'anken', 'created_dt')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    customer = models.ForeignKey(Customer, verbose_name='顧客管理ID', on_delete=models.CASCADE)
    customer_name = models.CharField(verbose_name='顧客名', max_length=200, blank=True, null=True)
    anken = models.ForeignKey(Anken, verbose_name='商談案件管理ID', on_delete=models.CASCADE)
    anken_name = models.CharField(verbose_name='商談案件名', max_length=200, blank=True, null=True)
    success_rate = models.FloatField(verbose_name='成約確率')
    created_dt = models.DateField(verbose_name='作成日付')

    def __str__(self):
        return 'ID:{0},CUSTOMER_NAME:{1},ANKEN_NAME:{2},CREATED_DT:{3}' \
        .format(self.id, self.customer_name, self.anken_name, self.created_dt)

# 管理者用画面での編集内容
class Anken_Successrt_History_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'customer_name', 'anken_name', 'success_rate', 'created_dt', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id',)
    search_fields = ('customer_name', 'anken_name', 'created_dt')

# 管理者画面に表示
admin.site.register(Anken_Successrt_History, Anken_Successrt_History_Admin)
