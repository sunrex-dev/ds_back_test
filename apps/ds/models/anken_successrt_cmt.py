from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.customer import *
from ..models.anken import *

class Anken_Successrt_Cmt(TenantBaseModel):
    """
案件成約確率コメントのテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_anken, ds_history, ds_customer より取得したデータを基にして更新する。
（ds_anken.result='継続'であるデータに紐づくanken_idが対象）
・全データを対象として、Delete + Insert を行う。
    """
    class Meta:
        db_table = 'ds_anken_successrt_cmt'
        verbose_name_plural = '案件成約確率コメント（ds_anken_successrt_cmt）'
        #unique_together = ('tenant', 'customer', 'anken', 'comment')

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
    comment = models.TextField(verbose_name='案件分析コメント')
    successup_rate = models.FloatField(verbose_name='成約上昇率')

    def __str__(self):
        return 'ID:{0},CUSTOMER_NAME:{1},ANKEN_NAME:{2},COMMENT:{3}' \
        .format(self.id, self.customer_name, self.anken_name, self.comment)

# 管理者用画面での編集内容
class Anken_Successrt_Cmt_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'customer_name', 'anken_name', 'comment', 'comment', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id',)
    search_fields = ('customer_name', 'anken_name', 'comment')

# 管理者画面に表示
admin.site.register(Anken_Successrt_Cmt, Anken_Successrt_Cmt_Admin)
