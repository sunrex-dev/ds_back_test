from django.db import models
from django.contrib import admin
from .process import Process

class Process_Logs(models.Model):
    """
PROCESS実行履歴テーブル
    """
    STATUS_CHOICES = (
        ('I', 'Infomation'),
        ('W', 'Warning'),
        ('E', 'Error'),
        ('C', 'Critical'),
        #('F', 'Fatal'),
    )

    class Meta:
        #db_table = "Process_logs"
        verbose_name_plural = 'PROCESS実行履歴（Process_logs）'

    process_id = models.IntegerField()
    process_name = models.CharField(max_length=100, null=True, blank=True)
    process_type = models.CharField(max_length=20, null=True, blank=True)
    tenant_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(null=True, blank=True, max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    process_log = models.TextField(null=True, blank=True, default='')

    def save(self, *args, **kwargs):
        try:
            process = Process.objects.get(id=self.process_id)
            self.process_name = process.name
            self.process_type = process.type
        except Process.DoesNotExist:
            pass
        super(Process_Logs, self).save(*args, **kwargs)
    
    def append_process_log(self, message):
        self.process_log += str(message) + '\n'

    def set_status(self, status):
        status = status.upper()
        if status == 'C':
            self.status = status
        elif status == 'E':
            if self.status != 'C':
                self.status = status
        elif status == 'W':
            if self.status != 'C' and self.status != 'E':
                self.status = status
        elif status == 'I':
            if self.status == '' or self.status == None:
                self.status = status

class Process_Logs_Admin(admin.ModelAdmin):
    list_display = ('id', 'process_id', 'process_name', 'tenant_id', 'status', 'created_at', 'updated_at')
    ordering = ('-id',)
    #readonly_fields = ('id', )
    list_filter = ('status', 'tenant_id',)
    search_fields = ('process_name', 'created_at', 'updated_at',)
    # 表示順序の指定
    fields = ['id', 'process_id', 'process_name', 'process_type', 'tenant_id', 'status', 'created_at', 'updated_at', 'process_log']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Process_Logs, Process_Logs_Admin)
