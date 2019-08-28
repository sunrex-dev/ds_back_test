from django.db import models
from django.contrib import admin
from apps.tenants.models import *

class Customer(TenantBaseModel):
    """
顧客情報のマスタテーブル
[更新説明]
・1回/日の間隔にて、Kintoneからデータを取得する。（特定期間中に更新があったデータが対象）
・noが同一であるデータがある場合はidをキーにしてUpdate、無ければInsertする。
    """
    class Meta:
        db_table = 'ds_customer'
        verbose_name_plural = '顧客情報（ds_customer）'
        unique_together = ('tenant', 'no')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    no = models.IntegerField(verbose_name='顧客番号')
    name = models.CharField(verbose_name='顧客名', max_length=200, blank=True, null=True)
    name_kana = models.CharField(verbose_name='顧客名カナ', max_length=200, blank=True, null=True)
    zip_code = models.CharField(verbose_name='郵便番号', max_length=10, blank=True, null=True)
    prefecture_name = models.CharField(verbose_name='都道府県', max_length=100, blank=True, null=True)
    city_name = models.CharField(verbose_name='市町村', max_length=100, blank=True, null=True)
    title = models.CharField(verbose_name='レコードタイトル', max_length=200, blank=True, null=True)
    updated_by = models.CharField(verbose_name='更新者名', max_length=50, blank=True, null=True)
    created_at_origin = models.DateTimeField(verbose_name='作成日時_元', blank=True, null=True)
    updated_at_origin = models.DateTimeField(verbose_name='更新日時_元', blank=True, null=True)
    hp_url = models.CharField(verbose_name='ホームページURL', max_length=2048, blank=True, null=True)
    sme_day = models.CharField(verbose_name='締日', max_length=3, blank=True, null=True)
    pay_month = models.CharField(verbose_name='支払月', max_length=3, blank=True, null=True)
    pay_day = models.CharField(verbose_name='支払日', max_length=3, blank=True, null=True)
    task = models.TextField(verbose_name='課題', max_length=2000, blank=True, null=True)
    products = models.CharField(verbose_name='取扱商品', max_length=200, blank=True, null=True)
    rank = models.CharField(verbose_name='顧客ランク', max_length=10, blank=True, null=True)
    needs = models.TextField(verbose_name='ニーズ', max_length=500, blank=True, null=True)
    yealy_sales = models.IntegerField(verbose_name='年商', blank=True, null=True)
    representative = models.CharField(verbose_name='代表者名', max_length=100, blank=True, null=True)
    manage_cd = models.CharField(verbose_name='顧客管理コード', max_length=20, blank=True, null=True)
    manage_name = models.CharField(verbose_name='顧客管理名', max_length=200, blank=True, null=True)
    settlement_month = models.CharField(verbose_name='決算月', max_length=3, blank=True, null=True)
    settlement = models.CharField(verbose_name='決定権者・決済額', max_length=300, blank=True, null=True)
    teikoku_data = models.CharField(verbose_name='帝国データバング', max_length=100, blank=True, null=True)
    industry_type = models.CharField(verbose_name='業種', max_length=100, blank=True, null=True)
    remark = models.TextField(verbose_name='会社情報備考', max_length=2000, blank=True, null=True)
    tel = models.CharField(verbose_name='電話番号', max_length=20, blank=True, null=True)
    fax = models.CharField(verbose_name='FAX番号', max_length=20, blank=True, null=True)
    employee_number = models.IntegerField(verbose_name='社員数', blank=True, null=True)

    def __str__(self):
        return 'ID:{0},NO:{1},NAME:{2}' \
        .format(self.id, self.no, self.name)

# 管理者用画面での編集内容
class Customer_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'no', 'name', 'prefecture_name', 'updated_at')
    ordering = ('tenant_id', 'no')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id',)
    search_fields = ('name', 'name_kana')

# 管理者画面に表示
admin.site.register(Customer, Customer_Admin)
