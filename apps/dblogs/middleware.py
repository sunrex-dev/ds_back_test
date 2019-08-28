from .models.access_logs import Access_Logs
from django.conf import settings
from django.utils import timezone
from apps.tenants.utils import tenant_info, user_info

class AccessLogsMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # create session
        if not request.session.session_key:
            request.session.create()

        access_logs_data = dict()

        # get the request path
        access_logs_data["path"] = request.path

        # get the client's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        access_logs_data["ip_address"] = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        access_logs_data["method"] = request.method
        access_logs_data["referrer"] = request.META.get('HTTP_REFERER',None)
        access_logs_data["session_key"] = request.session.session_key

        data = dict()
        data["get"] = dict(request.GET.copy())
        data['post'] = dict(request.POST.copy())

        # remove password form post data for security reasons
        keys_to_remove = ["password", "csrfmiddlewaretoken"]
        for key in keys_to_remove:
            data["post"].pop(key, None)

        access_logs_data["data"] = data
        access_logs_data["timestamp"] = timezone.now()

        tenant_obj=tenant_info.get_current_tenant()
        if tenant_obj:
            access_logs_data["tenant_id"] = tenant_obj.id
            access_logs_data["tenant_name"] = tenant_obj.name

        user_obj = user_info.get_current_user()
        if user_obj:
            access_logs_data["user_id"] = user_obj.id
            access_logs_data["user_name"] = user_obj.full_name

        try:
            Access_Logs(**access_logs_data).save()
        except Exception as e:
            pass

        response = self.get_response(request)
        return response
