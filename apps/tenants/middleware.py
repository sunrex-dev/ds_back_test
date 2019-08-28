from django.http import HttpResponse
from .utils import tenant_info, user_info

class SetCurrentTenantFromUser(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 前処理
        self.process_request(request)
        # ビューの処理
        response = self.get_response(request)
        # 後処理
        self.process_response(request, response)
        return response

#    def process_exception(self, request, exception): 
#        return HttpResponse("in exception")

    def process_request(self, request):

        host = request.get_host()
        if '://' in host:
            host = host.split('://')[1]
        if ':' in host:
            host = host.split(':')[0]
        subdomain = host.split('.')[0]

        from .models import Tenant
        try:
            tenant = Tenant.objects.get(subdomain_prefix=subdomain, is_active=True)
        except Tenant.DoesNotExist:
            tenant = None

        # 見つからない場合は開発中につき、localhostで再習得
        if tenant == None:
            subdomain = 'localhost'
            try:
                tenant = Tenant.objects.get(subdomain_prefix=subdomain, is_active=True)
            except Tenant.DoesNotExist:
                tenant = None


        tenant_info.set_current_tenant(tenant)
        #print(tenant)

        user = getattr(request, 'user', None)
        user_info.set_current_user(user)
        #print(user)

        return

    def process_response(self, request, response):
        tenant_info.set_current_tenant(None)
        user_info.set_current_user(None)
        return response

#def set_current_tenant(tenant):
#    setattr(_thread_locals, 'tenant', tenant)

#def get_current_tenant():
#    tenant = getattr(_thread_locals, 'tenant', None)
#    return getattr(_thread_locals, 'tenant', None)

#   def process_request(self, request):
#           if not hasattr(self, 'authenticator'):
#             from rest_framework_jwt.authentication import JSONWebTokenAuthentication
#             self.authenticator = JSONWebTokenAuthentication()
#             try:
#             user, _ = self.authenticator.authenticate(request)
#             except:
#             # TODO: handle failure
#             return
#             try:
#             #Assuming your app has a function to get the tenant associated for a user
#             current_tenant = get_tenant_for_user(user)
#             except:
#             # TODO: handle failure
#             return
#             set_current_tenant(current_tenant)

