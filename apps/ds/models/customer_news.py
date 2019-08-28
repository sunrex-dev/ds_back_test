from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.customer import *

class Customer_News(TenantBaseModel):
    """
顧客ニュースのテーブル
[更新説明]
・1回/日の間隔にて更新を行う。
・ds_history, ds_customer より取得したデータを基にして更新する。
（ds_customer_news.created_atが古い順に指定件数が対象）
・customer_id が同一であるデータがある場合は、customer_id単位で最初に1回 Deleteした上で、Insertする。
・customer_idに対する取得ニュースが0件である場合は、news_no=0をセットして、空レコードを登録する。
    """
    class Meta:
        db_table = 'ds_customer_news'
        verbose_name_plural = '顧客ニュース（ds_customer_news）'
        unique_together = ('tenant', 'customer', 'news_no')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    customer = models.ForeignKey(Customer, verbose_name='顧客管理ID', on_delete=models.CASCADE)
    customer_name = models.CharField(verbose_name='顧客名', max_length=200, blank=True, null=True)
    news_no = models.SmallIntegerField(verbose_name='ニュースNo')
    news_title = models.CharField(verbose_name='タイトル', max_length=200, blank=True, null=True)
    news_url = models.TextField(verbose_name='URL', max_length=2048, blank=True, null=True)
    news_sentiment = models.FloatField(verbose_name='感情値', default=0)
    news_semantic_role = models.TextField(verbose_name='要約', blank=True, null=True)

    def __str__(self):
        return 'ID:{0},CUSTOMER_NAME:{1},NEWS_NO:{2},NEWS_URL:{3}' \
        .format(self.id, self.customer_name, self.news_no, self.news_url)

# 管理者用画面での編集内容
class Customer_News_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'customer_name', 'news_url', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', )
    search_fields = ('customer_name', 'news_url')

# 管理者画面に表示
admin.site.register(Customer_News, Customer_News_Admin)
