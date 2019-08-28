from django.db import models
from django.contrib import admin

class Access_Logs(models.Model):
    """
アクセス履歴テーブル
    """
    #sys_id = models.AutoField(primary_key=True, null=False, blank=True)
    session_key = models.CharField(max_length=1024, null=False, blank=True)
    path = models.CharField(max_length=1024, null=False, blank=True)
    method = models.CharField(max_length=8, null=False, blank=True)
    data = models.TextField(null=True, blank=True)
    ip_address = models.CharField(max_length=45, null=False, blank=True)
    referrer = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(null=False, blank=True)
    tenant_id = models.IntegerField(null=True, blank=True)
    tenant_name = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=128, null=True, blank=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        #app_label = "django_server_access_logs"
        #db_table = "access_logs"
        verbose_name_plural = 'アクセス履歴（access_logs）'

class Access_Logs_Admin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'path', 'method', 'timestamp', 'tenant_name', 'user_name')
    ordering = ('-id',)
    #readonly_fields = ('id', )
    #list_filter = ('method', )
    search_fields = ('ip_address', 'path', 'tenant_name', 'user_id', 'user_name')

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        # Nobody is allowed to add
        return False

    def has_delete_permission(self, request, obj=None):
        # Nobody is allowed to delete
        return False

admin.site.register(Access_Logs, Access_Logs_Admin)
