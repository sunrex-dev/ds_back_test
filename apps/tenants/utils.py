from threading import local

_thread_locals = local()

class tenant_info():
    def set_current_tenant(tenant):
        setattr(_thread_locals, 'tenant', tenant)

    def get_current_tenant():
        #tenant = getattr(_thread_locals, 'tenant', None)
        return getattr(_thread_locals, 'tenant', None)

    def set_current_tenant_by_id(tenant_id):
        from .models import Tenant
        try:
            tenant = Tenant.objects.get(id=tenant_id, is_active=True)
        except Tenant.DoesNotExist:
            tenant = None
        setattr(_thread_locals, 'tenant', tenant)

class user_info():
    def set_current_user(user):
        if user != None and user.id == None:
            user = None
            #print('set_current_user is None')
        setattr(_thread_locals, 'user', user)

    def get_current_user():
        #user = getattr(_thread_locals, 'user', None)
        return getattr(_thread_locals, 'user', None)
