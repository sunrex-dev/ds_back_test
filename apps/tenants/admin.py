from django.contrib import admin
from .models import Tenant

class TenantModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subdomain_prefix', 'created_at', 'is_active' )
    ordering = ('id',)
    #readonly_fields = ('id', 'created_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'created_at']
        else:
            return ['created_at']

admin.site.register(Tenant, TenantModelAdmin)
