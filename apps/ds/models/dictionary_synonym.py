from django.db import models
from django.contrib import admin
from apps.tenants.models import *
from ..models.dictionary import *
from apps.ds.models.dictionary import Dictionary

class Dictionary_Synonym(TenantBaseModel):
    """
辞書類似ワードのテーブル
[更新説明]
・辞書管理画面での随時更新、又は1回/日の間隔にて学習用の更新を行う。
・更新時は、dictonary_idをキーにしてDelete + Insertを行う。
    """
    class Meta:
        db_table = 'ds_dictionary_synonym'
        verbose_name_plural = '辞書類似ワード（ds_dictionary_synonym）'
        unique_together = ('tenant', 'dictionary', 'no')

    # フィールド定義（制御用）
    id = models.AutoField(verbose_name='ID', primary_key=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    lock_id = models.IntegerField(verbose_name='LOCK ID', default=0)
    # フィールド定義（データ格納用）
    dictionary = models.ForeignKey(Dictionary, verbose_name='辞書管理ID', on_delete=models.CASCADE)
    dictionary_grpname = models.CharField(verbose_name='辞書グループ名', max_length=200, blank=True, null=True)
    dictionary_distword = models.CharField(verbose_name='辞書キーワード', max_length=200, blank=True, null=True)
    no = models.SmallIntegerField(verbose_name='類似ワードNo')
    synonymword = models.CharField(verbose_name='類似ワード', max_length=200)

    def __str__(self):
        return 'ID:{0},DICTIONARY_GRPNAME:{1},DICTIONARY_DISTWORD:{2},NO:{3},SYNONYMWORD:{4}' \
        .format(self.id, self.dictionary_grpname, self.dictionary_distword, self.NO, self.synonymword)

# 管理者用画面での編集内容
class Dictionary_Synonym_Admin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'dictionary_grpname', 'dictionary_distword', 'no', 'synonymword', 'updated_at')
    ordering = ('tenant_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('tenant_id', )
    search_fields = ('dictionary_grpname', 'dictionary_distword', 'synonymword')

# 管理者画面に表示
admin.site.register(Dictionary_Synonym, Dictionary_Synonym_Admin)
