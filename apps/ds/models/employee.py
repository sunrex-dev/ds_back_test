from django.db import models
from django.contrib import admin
from apps.tenants.models import *

class Employee(TenantBaseModel):
    """
社員情報のマスタテーブル
[更新説明]
・1回/日の間隔にて、Kintoneからデータを取得する。
・noが同一であるデータがある場合はidをキーにしてUpdate、無ければInsertする。
    """
    class Meta:
        db_table = 'ds_employee'
        verbose_name_plural = '社員情報（ds_employee）'
        unique_together = ('tenant', 'no')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    no = models.IntegerField(verbose_name='社員管理番号')
    code = models.CharField(verbose_name='社員コード', max_length=20)
    code_short = models.CharField(verbose_name='社員コード省略版', max_length=20, blank=True, null=True)
    name = models.CharField(verbose_name='社員名', max_length=200, blank=True, null=True)
    name_kana = models.CharField(verbose_name='社員名カナ', max_length=200, blank=True, null=True)
    name_search = models.CharField(verbose_name='社員名検索用', max_length=200, blank=True, null=True)
    department = models.CharField(verbose_name='所属部署', max_length=50, blank=True, null=True)
    created_at_origin = models.DateTimeField(verbose_name='作成日時_元', blank=True, null=True)
    updated_at_origin = models.DateTimeField(verbose_name='更新日時_元', blank=True, null=True)
    deleted_kbn = models.CharField(verbose_name='廃止区分', max_length=20, blank=True, null=True)
    deleted_at = models.DateTimeField(verbose_name='廃止日時', blank=True, null=True)

    def __str__(self):
        return 'ID:{0},NO:{1},NAME:{2},CODE:{3}' \
        .format(self.id, self.no, self.name, self.code)

# 管理者用画面での編集内容
class Employee_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'no', 'name', 'code', 'department', 'deleted_kbn', 'updated_at')
    ordering = ('tenant_id', 'code')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id',)
    search_fields = ('name', 'name_kana', 'department', 'code')

# 管理者画面に表示
admin.site.register(Employee, Employee_Admin)
