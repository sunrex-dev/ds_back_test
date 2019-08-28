from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.employee import *
from ..models.customer import *

class Anken(TenantBaseModel):
    """
商談案件のテーブル
[更新説明]
・1回/日の間隔にて、Kintoneからデータを取得する。（特定期間中に更新があったデータが対象）
・noが同一であるデータがある場合はidをキーにしてUpdate、無ければInsertする。
    """
    class Meta:
        db_table = 'ds_anken'
        verbose_name_plural = '商談案件（ds_anken）'
        unique_together = ('tenant', 'no')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    no = models.IntegerField(verbose_name='商談案件番号')
    name = models.CharField(verbose_name='商談案件名', max_length=200, blank=True, null=True)
    title = models.CharField(verbose_name='レコードタイトル', max_length=200, blank=True, null=True)
    created_at_origin = models.DateTimeField(verbose_name='作成日時_元', blank=True, null=True)
    updated_at_origin = models.DateTimeField(verbose_name='更新日時_元', blank=True, null=True)
    employee = models.ForeignKey(Employee, verbose_name='社員管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    employee_no = models.IntegerField(verbose_name='社員管理番号', blank=True, null=True)
    employee_name = models.CharField(verbose_name='営業担当社員名', max_length=50, blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name='顧客管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    customer_no = models.IntegerField(verbose_name='顧客番号')
    customer_name = models.CharField(verbose_name='顧客名', max_length=200, blank=True, null=True)
    section_name = models.CharField(verbose_name='顧客部署名', max_length=200, blank=True, null=True)
    section_tel_type = models.CharField(verbose_name='顧客部署TEL種類', max_length=100, blank=True, null=True)
    section_tel = models.CharField(verbose_name='顧客部署TEL番号', max_length=20, blank=True, null=True)
    customer_person = models.CharField(verbose_name='顧客側担当', max_length=50, blank=True, null=True)
    close_plan_dt = models.DateField(verbose_name='成約予定日', blank=True, null=True)
    close_plan_total = models.IntegerField(verbose_name='成約予定金額合計')
    close_plan_profit = models.IntegerField(verbose_name='成約予定粗利合計')
    close_plan_mamount = models.IntegerField(verbose_name='成約予定月額合計')
    close_dt = models.DateField(verbose_name='成約計上日', blank=True, null=True)
    sales_plan_dt = models.DateField(verbose_name='売上予定日（1回目）', blank=True, null=True)
    sales_plan_profit = models.IntegerField(verbose_name='売上予定粗利合計')
    sales_plan_mamount = models.IntegerField(verbose_name='売上予定月額合計')
    result = models.CharField(verbose_name='結果', max_length=20, blank=True, null=True)
    result_analyze = models.TextField(verbose_name='結果分析', max_length=2000, blank=True, null=True)
    remarks = models.TextField(verbose_name='備考', max_length=2000, blank=True, null=True)
    salse_probability = models.SmallIntegerField(verbose_name='成約確率')
    result_kbn = models.SmallIntegerField(verbose_name='結果区分',help_text='0:未案件,1:継続,2:成約,3:敗戦',default=0)

    def __str__(self):
        return 'ID:{0},NO:{1},NAME:{2}' \
        .format(self.id, self.no, self.name)

# 管理者用画面での編集内容
class Anken_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'no', 'name', 'close_plan_dt', 'employee_name', 'result', 'updated_at')
    ordering = ('tenant_id', '-no')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id',)
    search_fields = ('name', 'employee_name', 'title')

# 管理者画面に表示
admin.site.register(Anken, Anken_Admin)
