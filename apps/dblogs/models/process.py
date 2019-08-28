from django.db import models
from django.contrib import admin

class Process(models.Model):
    """
PROCESS管理テーブル
    """
    PRC_TYPE_CHOICES = (
        ('RestAPI', 'REST API'),
        ('BGJob', 'Back Ground Job'),
        ('Etc', 'その他'),
    )
    class Meta:
        #db_table = "Process"
        verbose_name_plural = 'PROCESS管理（Process）'
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=PRC_TYPE_CHOICES)
    comment = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Process_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'created_at', 'updated_at', 'comment')
    ordering = ('id',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('type',)
    search_fields = ('name', 'comment',)

admin.site.register(Process, Process_Admin)
