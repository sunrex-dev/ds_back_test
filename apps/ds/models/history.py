from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.customer import *
from ..models.anken import *
from ..models.employee import *

class History(TenantBaseModel):
    """
商談履歴のテーブル
[更新説明]
・1回/日の間隔にて、Kintoneからデータを取得する。（特定期間中に更新があったデータが対象）
・noが同一であるデータがある場合はidをキーにしてUpdate、無ければInsertする。
    """
    class Meta:
        db_table = 'ds_history'
        verbose_name_plural = '商談履歴（ds_history）'
        unique_together = ('tenant', 'no')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    no = models.IntegerField(verbose_name='商談履歴番号')
    anken = models.ForeignKey(Anken, verbose_name='商談案件管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    anken_no = models.IntegerField(verbose_name='商談案件番号', blank=True, null=True)
    anken_name = models.CharField(verbose_name='商談案件名', max_length=200, blank=True, null=True)
    title = models.CharField(verbose_name='レコードタイトル', max_length=200, blank=True, null=True)
    created_at_origin = models.DateTimeField(verbose_name='作成日時_元', blank=True, null=True)
    updated_at_origin = models.DateTimeField(verbose_name='更新日時_元', blank=True, null=True)
    employee = models.ForeignKey(Employee, verbose_name='社員管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    employee_no = models.IntegerField(verbose_name='社員管理番号', blank=True, null=True)
    employee_name = models.CharField(verbose_name='営業担当社員名', max_length=50, blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name='顧客管理ID', null=True, on_delete=models.DO_NOTHING, db_constraint=False)
    customer_no = models.IntegerField(verbose_name='顧客番号')
    customer_name = models.CharField(verbose_name='顧客名', max_length=200, blank=True, null=True)
    visit_plan_dt = models.DateTimeField(verbose_name='訪問予定日時', blank=True, null=True)
    visit_plan_times = models.SmallIntegerField(verbose_name='訪問時間（予定）', blank=True, null=True)
    visit_dt = models.DateTimeField(verbose_name='実訪問日時', blank=True, null=True)
    visit_times = models.SmallIntegerField(verbose_name='訪問時間（実績）', blank=True, null=True)
    purpose = models.TextField(verbose_name='面談目的', max_length=2000, blank=True, null=True)
    meet_method = models.CharField(verbose_name='面談手段（予定）', max_length=100, blank=True, null=True)
    meet_result = models.CharField(verbose_name='面談手段（実績）', max_length=100, blank=True, null=True)
    result = models.TextField(verbose_name='面談結果', max_length=10000, blank=True, null=True)
    remarks = models.TextField(verbose_name='備考', max_length=10000, blank=True, null=True)
    future_issue = models.TextField(verbose_name='課題', max_length=10000, blank=True, null=True)
    next_action = models.TextField(verbose_name='次回設定', max_length=10000, blank=True, null=True)
    next_action_dt = models.DateTimeField(verbose_name='次回アクション日時', blank=True, null=True)
    attention = models.CharField(verbose_name='注目', max_length=10, blank=True, null=True)
    good_count = models.SmallIntegerField(verbose_name='いいね数', blank=True, null=True)

    def __str__(self):
        return 'ID:{0},NO:{1},TITLE:{2}' \
        .format(self.id, self.no, self.title)

# 管理者用画面での編集内容
class History_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'no', 'visit_dt', 'employee_name', 'customer_name', 'purpose', 'result', 'visit_times')
    ordering = ('tenant_id', '-visit_dt')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id',)
    search_fields = ('customer_name', 'employee_name', 'title')

# 管理者画面に表示
admin.site.register(History, History_Admin)
