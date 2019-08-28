
from django.db import models
from django.utils import timezone
from .utils import tenant_info

class Tenant(models.Model):
    class Meta:
        verbose_name_plural = 'テナント設定（tenants_tenant）'
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    subdomain_prefix = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(verbose_name='有効', default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{0}:{1}'.format(self.id, self.name)

class TenantManager(models.Manager):
    def get_queryset(self):
        tenant_id = -1
        current_tenant=tenant_info.get_current_tenant()
        if current_tenant:
            tenant_id = current_tenant.id
        #print('TenantManager get_queryset tenant_id = '+str(tenant_id))
        if tenant_id == 0:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(tenant_id=tenant_id)

class TenantBaseModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    objects = TenantManager()

#    def _do_insert(self, manager, using, fields, update_pk, raw):
#        return super(TenantBaseModel, self)._do_insert(self, manager, using, fields, update_pk, raw)
    def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
        current_tenant=tenant_info.get_current_tenant()
        if current_tenant:
            tenant_id = current_tenant.id
            base_qs = base_qs.filter(tenant_id=tenant_id)
        return super(TenantBaseModel, self)._do_update(base_qs, using, pk_val, values, update_fields, forced_update)

    class Meta:
        abstract = True
